from pickle import TRUE
from pandas import DataFrame
from .strategy import Strategy
from .constants import BUY_INDICATOR, NO_TRANSACTION_INDICATOR
from .utils import make_transaction_series


class BuyAndHold(Strategy):
    def __init__(self) -> None:
        super().__init__()
        self.bought = False

    def generate_transaction(self, row):
        indicator = NO_TRANSACTION_INDICATOR

        if not self.bought:
            indicator = BUY_INDICATOR
            self.bought = TRUE

        return make_transaction_series(indicator, self.buy_percentage)

    def setup_dataframe(self, df) -> DataFrame:
        return df
