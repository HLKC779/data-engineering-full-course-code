import sqlite3
import pandas as pd

# Extract
orders = pd.read_csv("data/orders.csv")
items = pd.read_csv("data/order_items.csv")
products = pd.read_csv("data/products.csv")
print(orders.shape)
print(orders.dtypes)

# Transform
orders = orders.drop_duplicates(subset="order_id")
orders["order_date"] = pd.to_datetime(orders["order_date"])
print("Missing amounts:", orders["amount"].isna().sum())
completed = orders[orders["status"] == "completed"]

lines = items.merge(completed, on="order_id", validate="many_to_one")
lines = lines.merge(products, on="product_id", validate="many_to_one", suffixes=("", "_product"))
lines["revenue"] = lines["quantity"] * lines["unit_price"]
by_cat = (lines.groupby("category", as_index=False)["revenue"].sum()
    .sort_values("revenue", ascending=False))
print(by_cat)

# Load
with sqlite3.connect("shop.db") as con:
    by_cat.to_sql("revenue_by_category", con, if_exists="replace", index=False)
    check = pd.read_sql("SELECT COUNT(*) AS n FROM revenue_by_category", con)
    print("Rows in database:", check["n"][0])