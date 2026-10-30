import pandas as pd
from transforms import clean_orders


def make(rows):
    return pd.DataFrame(rows, columns=["order_id", "status", "amount"])


def test_removes_duplicates():
    df = make([(1, "completed", 5.0), (1, "completed", 5.0)])
    assert len(clean_orders(df)) == 1


def test_drops_missing_amounts():
    df = make([(1, "completed", None), (2, "completed", 3.0)])
    assert clean_orders(df)["order_id"].tolist() == [2]


def test_keeps_latest_version():
    df = make([(1, "completed", 5.0), (1, "refunded", 5.0)])
    assert clean_orders(df)["status"].tolist() == ["refunded"]