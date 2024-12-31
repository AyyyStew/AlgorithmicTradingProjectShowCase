import json
from uuid import uuid4
from pandas import DataFrame, to_datetime
import decimal


def candlestick_dict_to_dataframe(candlesticks: dict):
    df = DataFrame.from_records(candlesticks)
    df["start"] = df["start"].astype(int)
    df["start"] = to_datetime(df["start"])
    df = df.set_index("start")
    df = df.reindex(index=df.index[::-1])
    return df


def add_ema(df: DataFrame, ema_value: int, column_name: str, value: str = "close"):
    df[column_name] = df[value].ewm(span=ema_value).mean()
    return df


def json_to_file(filename, data):
    with open(filename, "w") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def generate_id():
    return str(uuid4())


def round_down(value: str, decimals: int) -> str:
    with decimal.localcontext() as ctx:
        d = decimal.Decimal(value)
        ctx.rounding = decimal.ROUND_DOWN
        return str(round(d, decimals))
