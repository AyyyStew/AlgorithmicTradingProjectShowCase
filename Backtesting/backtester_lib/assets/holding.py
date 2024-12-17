from .asset import Asset
from ..ticker import Ticker


class Holding(Asset):
    def __init__(
        self,
        ticker: Ticker,
        starting_balance: float = 1000,
        qty: float = 0,
        buy_fee: float = 0.005,
        sell_fee: float = 0.005,
    ):
        super().__init__(starting_balance, qty, buy_fee, sell_fee)
        self.ticker = ticker
