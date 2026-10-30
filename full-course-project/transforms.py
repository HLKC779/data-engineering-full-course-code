import pandas as pd


def clean_orders(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df.copy()

    if "order_id" not in df.columns or "amount" not in df.columns:
        raise KeyError("DataFrame must contain 'order_id' and 'amount' columns")

    cleaned = df.drop_duplicates(subset="order_id", keep="last").copy()

    def is_missing(value):
        if pd.isna(value):
            return True
        if isinstance(value, str):
            return value.strip() == ""
        return False

    cleaned = cleaned[~cleaned["amount"].map(is_missing)].copy()
    return cleaned.reset_index(drop=True)