from abc import ABC, abstractmethod
from pandas import Series, DataFrame


class Strategy(ABC):
    @abstractmethod
    def __init__(self, buy_percentage=1, sell_percentage=1) -> None:
        super().__init__()
        self.buy_percentage = buy_percentage
        self.sell_percentage = sell_percentage

    @abstractmethod
    def generate_transaction(self, row) -> Series:
        pass

    @abstractmethod
    def setup_dataframe(self, df) -> DataFrame:
        return df
