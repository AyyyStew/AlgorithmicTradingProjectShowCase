import asyncio
import json
import logging
from datetime import datetime, timedelta
from scheduler import start
from pandas import DataFrame

# Custom
from strategies.strategy import Strategy
import utils
import database
from api import api
from secret_config import COINBASE_API_KEY, COINBASE_API_SECRET
from config import debug


async def get_balance(account_id):
    response = await api.get_account(account_id)
    return response["data"]["balance"]["amount"]


async def get_price(product_id):
    response = await api.get_product(product_id)
    return response["price"]


async def get_last_transaction():
    last_order = database.get_latest_order()
    # if there is a last order in the database
    if last_order:
        logging.info("Found last order")
        last_transaction = last_order.transaction_type
    else:
        logging.info(
            "Latest Order not found, continuing with last transaction as a sell order"
        )
        last_transaction = "SELL"

    return last_transaction.upper()


async def get_candle_df(product_id):
    # get today and 75 days prior
    start = datetime.now() - timedelta(days=75)
    end = datetime.now()
    # get candles
    candles_result = await api.get_candles(product_id, start, end)
    # convert to dataframe
    df = utils.candlestick_dict_to_dataframe(candles_result["candles"])
    return df


async def buy(product_id, price, btc_balance, usdc_balance):
    logging.info("Starting Buying Procedure")
    id = utils.generate_id()
    trading_amount = utils.round_down(usdc_balance, 2)
    logging.info(f"Trading {trading_amount} USDC")
    res = await api.market_buy(id, product_id, str(trading_amount))
    coinbase_id = res.get("success_response", {}).get("order_id")

    order_id = database.create_order(
        id,
        coinbase_id,
        "BUY",
        product_id,
        price,
        datetime.now(),
        btc_balance,
        usdc_balance,
        await get_balance("BTC"),
        await get_balance("USDC"),
        json.dumps(res),
    )
    logging.info(f"Finished Buying Procedure, order_id: {order_id}")
    return order_id


async def sell(product_id, price, btc_balance, usdc_balance):
    logging.info("Starting Selling Procedure")

    id = utils.generate_id()
    res = await api.market_sell(id, product_id, btc_balance)
    coinbase_id = res.get("success_response", {}).get("order_id")
    order_id = database.create_order(
        id,
        coinbase_id,
        "SELL",
        product_id,
        price,
        datetime.now(),
        btc_balance,
        usdc_balance,
        await get_balance("BTC"),
        await get_balance("USDC"),
        json.dumps(res),
    )
    logging.info(f"Finished Selling Procedure, order_id: {order_id}")
    return order_id


async def generateSignals(df):
    strategy = Strategy()

    ema_values = (5, 8, 13, 50)
    df: DataFrame = strategy.setup_dataframe(df)
    logging.debug(df.tail(1))
    buy_signal = strategy.generate_buy_signal(df.tail(1).squeeze())
    sell_signal = strategy.generate_sell_signal(df.tail(1).squeeze())

    return (buy_signal, sell_signal)


async def main():
    logging.info("Starting")
    product_id = "BTC-USDC"
    buy_percent = 1

    df = await get_candle_df(product_id=product_id)
    buy_signal, sell_signal = await generateSignals(df)

    logging.info(f"Buy signal: {buy_signal}")
    logging.info(f"Sell signal: {sell_signal}")
    logging.info("Finished Calculations")

    last_transaction = await get_last_transaction()

    if debug:
        logging.debug(repr(database.get_latest_order()))

    logging.info(f"Last Transaction Type: {last_transaction}")

    should_buy = buy_signal and last_transaction == "SELL"
    should_sell = last_transaction == "BUY" and sell_signal

    btc_balance = await get_balance("BTC")
    usdc_balance = await get_balance("USDC")
    price = await get_price(product_id)

    if should_buy:
        logging.debug("Entering Buy Branch")
        if debug:
            logging.debug("Debug is true, Will not buy")
        else:
            order_id = await buy(product_id, price, btc_balance, usdc_balance)

    elif should_sell:
        logging.debug("Entering Sell Branch")
        if debug:
            logging.debug("Debug is true. Will not sell.")
        else:
            order_id = await sell(product_id, price, btc_balance, usdc_balance)
    else:
        logging.info("No transaction at this time")

    logging.info("Finished")


if __name__ == "__main__":
    level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(
        filename="bot.log",
        encoding="utf-8",
        level=level,
        format="%(asctime)s %(message)s",
        datefmt="%m/%d/%Y %I:%M:%S %p",
    )

    logging.getLogger().addHandler(logging.StreamHandler())
    if debug:
        asyncio.run(main())
    else:
        # Every Hour
        asyncio.run(start(main, "0 * * * *"))
