from typing import Callable, List
from datetime import datetime
from functools import cache

from backtester_lib.strategies.strategy import Strategy
from backtester_lib.ticker import Ticker
from backtester_lib.assets.holding import Holding
from backtester_lib.strategy_tester import StrategyTester


class TestRunner:
    def __init__(
        self,
        ticker: Ticker,
        start_date: datetime,
        end_date: datetime,
        strategies: List[tuple[str, Strategy]],
        pricing_functions: List[tuple[str, Callable, Callable, Callable]],
    ) -> None:
        self.strategies = strategies
        self.ticker = ticker
        self.pricing_functions = pricing_functions
        self.start_date = start_date
        self.end_date = end_date
        self.test_results = {}

    def set_date_range(self, start_date: datetime, end_date: datetime):
        self.start_date = start_date
        self.end_date = end_date

    # @cache
    def run_tests(self, holding: Holding | None = None):
        results = {}
        for strat_name, strategy in self.strategies:
            strat_results = {}
            for pricing_name, buy, sell, value in self.pricing_functions:
                holding = Holding(self.ticker) if holding == None else holding
                test = StrategyTester(
                    f"{strat_name}",
                    strategy,
                    holding,
                )
                df, test_result = test.run_test(
                    f"{strat_name}",
                    self.start_date,
                    self.end_date,
                    sell,
                    buy,
                    value,
                )
                strat_results[pricing_name] = df[f"{strat_name}"]
                self.test_results[f"{strat_name}"] = test_result

            results[strat_name] = strat_results

        self.results = results

        return results

    def get_plot(self, pricings: List["str"]):
        df = self.ticker.dataframe.copy()
        df = df[self.start_date : self.end_date]
        lines = []

        for strat, result in self.results.items():
            for pricing in pricings:
                line_name = f"{strat}: {pricing}"
                lines.append(line_name)
                df[line_name] = result[pricing]

        plt = df.plot(y=[name for name in lines], kind="line")

        return plt
