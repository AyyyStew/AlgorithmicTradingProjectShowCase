import pandas
from dataclasses import dataclass
from .constants import SAMPLING_PERIOD_OPTIONS


# Class to hold pandas dataframe of stock values.
# The class reads in a csv file of the stock values. via the path_to_csv parameter
# The csv should have the following headers:
# open, high, low, close, date
@dataclass
class Ticker:
    def __init__(
        self, name: str, path_to_csv: str, period: SAMPLING_PERIOD_OPTIONS
    ) -> None:
        self.name = name
        self.dataframe = pandas.read_csv(path_to_csv)
        self.dataframe["date"] = pandas.to_datetime(self.dataframe["time"], unit="s")
        self.dataframe.set_index("date", inplace=True)
        self.period = period
