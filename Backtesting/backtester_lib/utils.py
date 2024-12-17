import pandas
import random
from datetime import datetime, timedelta

# pricing functions
open_close_average_pricing = lambda row: (row["open"] + row["close"]) / 2
open_pricing = lambda row: row["open"]
close_pricing = lambda row: row["close"]
high_pricing = lambda row: row["high"]
low_pricing = lambda row: row["low"]
high_low_average = lambda row: (row["high"] + row["low"]) / 2


def convert_epoch_to_datetime(
    df, epoch_column_name="time", datetime_column_name="date"
):
    df[datetime_column_name] = pandas.to_datetime(df[epoch_column_name], unit="s")
    return df


def generate_random_date_ranges(
    start_date: datetime,
    end_date: datetime,
    num_ranges: int,
    min_range_days: int = 2,
    max_range_days: int = None,
):
    date_ranges = []

    for _ in range(num_ranges):
        # Generate a random start date within the overall range
        max_days = (end_date - start_date).days - min_range_days
        if max_range_days is not None:
            max_days = min(max_days, max_range_days)

        random_start = start_date + timedelta(days=random.randint(0, max_days))

        # Generate a random end date ensuring the minimum range requirement is met
        max_end_days = (end_date - random_start).days
        if max_range_days is not None:
            max_end_days = min(max_end_days, max_range_days)

        random_end = random_start + timedelta(
            days=random.randint(min_range_days, max_end_days)
        )

        # Add the random date range to the list
        date_ranges.append((random_start, random_end))

    return date_ranges
