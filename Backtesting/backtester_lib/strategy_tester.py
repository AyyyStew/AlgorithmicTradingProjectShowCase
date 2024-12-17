from dataclasses import dataclass
from functools import cache
from itertools import pairwise
from datetime import datetime
from typing import Tuple, Callable
from pandas import DataFrame, concat, Series

from .assets.holding import Holding
from .strategies.strategy import Strategy
from .strategies.constants import (
    BUY_INDICATOR,
    SELL_INDICATOR,
    NO_TRANSACTION_INDICATOR,
)


@dataclass
class TestResult:
    name: str
    data_source: str
    start_date: datetime
    end_date: datetime
    num_buys: int
    num_sells: int
    start_balance: float
    end_balance: float

    @property
    def num_transactions(self):
        return self.num_buys + self.num_sells

    @property
    def net_return(self):
        return self.end_balance - self.start_balance

    @property
    def return_on_investment(self):
        """https://www.investopedia.com/articles/basics/10/guide-to-calculating-roi.asp
        roi = (final_value - cost) / cost
        It returns a decimal percentage. .5 is a 50% return.
        """
        return self.net_return / self.start_balance

    @property
    def annualized_return_on_investment(self):
        """Returns a decimal percentage. .5 is a 50% annualized return."""
        return self.return_on_investment / (
            (self.end_date - self.start_date).days / 365.25
        )


class StrategyTester:
    def __init__(self, test_name: str, strategy: Strategy, holding: Holding) -> None:
        self.strategy = strategy
        self.holding = holding
        self.name = test_name

    # @cache
    def run_test(
        self,
        name=None,
        start_date=None,
        end_date=None,
        sell_pricing_function=lambda row: row["open"],
        buy_pricing_function=lambda row: row["open"],
        portfolio_value_pricing_function=lambda row: row["close"],
        buy_on_next=False,
    ) -> Tuple[DataFrame, TestResult]:
        df = self.holding.ticker.dataframe.copy()

        df = df[start_date:end_date]
        df = self.strategy.setup_dataframe(df)

        res = df.apply(self.strategy.generate_transaction, axis=1)
        df = concat([df, res], axis=1)

        def process_row(row, next, buy_on_next=False):
            price = None
            transaction = row["transaction"]
            percent_to_trade = row["percent_to_trade"]

            row_to_apply = next if buy_on_next else row
            if transaction == NO_TRANSACTION_INDICATOR:
                # No transaction should be the most common, move it first to only do one check
                pass
            elif transaction == BUY_INDICATOR:
                self.holding.buy(buy_pricing_function(row_to_apply), percent_to_trade)

            elif transaction == SELL_INDICATOR:
                self.holding.sell(sell_pricing_function(row_to_apply), percent_to_trade)

            price = portfolio_value_pricing_function(next)
            holding_value = self.holding.get_holding_value(price)
            return holding_value

        # df[self.name] = df.apply(process_row, axis=1)
        result = [
            process_row(row[1], next[1], buy_on_next=buy_on_next)
            for row, next in pairwise(df.iterrows())
        ]
        result.append(result[-1])
        result_series = Series(result, index=df.index)

        df[name] = result_series

        result = TestResult(
            name=name,
            data_source=self.holding.ticker.name,
            start_date=df.head(n=1).index.item(),
            end_date=df.tail(n=1).index.item(),
            num_buys=df["transaction"].value_counts().get("buy", 0),
            num_sells=df["transaction"].value_counts().get("sell", 0),
            start_balance=df.head(n=1).get(name, "").item(),
            end_balance=df.tail(n=1).get(name, "").item(),
        )

        self.holding.reinitialize()
        return (df, result)
