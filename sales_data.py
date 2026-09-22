import pandas as pd


def load_sales_data(path: str) -> pd.DataFrame:
    return pd.read_csv(path, parse_dates=["date"])


def get_total_sales(df: pd.DataFrame) -> float:
    return df["total_amount"].sum()


def get_total_orders(df: pd.DataFrame) -> int:
    return len(df)
