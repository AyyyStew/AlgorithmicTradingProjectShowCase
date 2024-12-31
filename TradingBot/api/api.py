from typing import final
from functools import partial
from datetime import datetime, timedelta
import json
import requests
from .auth import auth


# sign in with coinbase api version 2
# used to use sign in with coinbase api
siwc_api_v2: final = "https://api.coinbase.com/v2"
advanced_trade_api: final = "https://api.coinbase.com/api/v3"
request = partial(requests.request, auth=auth)
get = partial(requests.get, auth=auth)
post = partial(requests.post, auth=auth)


# async def get_user():
#     r = get(siwc_api_v2 + "/user")
#     return r.json()
# async def get_accounts():
#     r = get(siwc_api_v2 + "/accounts")
#     return r.json()
# async def create_account(product):
#     r = get(f"{siwc_api_v2}/accounts/{product}")
#     return r.json()
# async def get_account(id):
#     r = get(f"{siwc_api_v2}/accounts/{id}")
#     return r.json()
# async def get_product(product_id):
#     r = get(advanced_trade_api + "/brokerage/products/" + product_id)
#     return r.json()
# async def get_addresses(account_id):
#     r = get(f"{siwc_api_v2}/accounts/{account_id}/addresses")
#     return r.json()
# async def get_address(account_id, address_id):
#     r = get(f"{siwc_api_v2}/accounts/{account_id}/addresses/{address_id}")
#     return r.json()
# /


async def market_buy(order_id, product_id, quote_size):
    data = {
        "client_order_id": str(order_id),
        "product_id": product_id,
        "side": "BUY",
        "order_configuration": {"market_market_ioc": {"quote_size": str(quote_size)}},
    }
    strung = json.dumps(data)

    r = post(f"{advanced_trade_api}/brokerage/orders", data=json.dumps(data))
    return r.json()


async def market_sell(order_id, product_id, base_size):
    data = {
        "client_order_id": str(order_id),
        "product_id": product_id,
        "side": "SELL",
        "order_configuration": {"market_market_ioc": {"base_size": str(base_size)}},
    }
    strung = json.dumps(data)

    r = post(f"{advanced_trade_api}/brokerage/orders", data=json.dumps(data))
    return r.json()


async def get_candles(
    product_id: str,
    start_date: datetime,
    end_date: datetime = datetime.now(),
    granularity: str = "ONE_DAY",
):
    params = {
        "start": str(int(start_date.timestamp())),
        "end": str(int(end_date.timestamp())),
        "granularity": granularity,
    }

    r = get(
        f"{advanced_trade_api}/brokerage/products/{product_id}/candles", params=params
    )
    return r.json()


async def get_products():
    r = get(advanced_trade_api + "/brokerage/products")
    return r.json()


async def get_account(id):
    r = get(f"{siwc_api_v2}/accounts/{id}")
    return r.json()


async def get_product(product_id):
    r = get(advanced_trade_api + "/brokerage/products/" + product_id)
    return r.json()
