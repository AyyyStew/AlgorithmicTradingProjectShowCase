from pandas import Series
from .constants import NO_TRANSACTION_INDICATOR


def make_transaction_series(transaction, percent_to_trade):
    how_much_to_trade = percent_to_trade
    if transaction == NO_TRANSACTION_INDICATOR:
        percent_to_trade = 0

    return Series([transaction, how_much_to_trade], ["transaction", "percent_to_trade"])
