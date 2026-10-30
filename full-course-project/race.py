import time
import duckdb
import pandas as pd
import polars as pl

FILE = "data/nyc/yellow_tripdata_2024-01.parquet"

start = time.perf_counter()
df = pd.read_parquet(FILE, columns=["payment_type", "fare_amount", "tip_amount"])
df = df[df["fare_amount"] > 0]
res = df.groupby("payment_type").agg(trips=("tip_amount", "size"), avg_tip=("tip_amount", "mean"))
print(f"pandas: {time.perf_counter() - start:.2f} s")
start = time.perf_counter()
res = (pl.scan_parquet(FILE)
    .filter(pl.col("fare_amount") > 0)
    .group_by("payment_type")
    .agg(pl.len().alias("trips"), pl.col("tip_amount").mean().round(2).alias("avg_tip"))
    .sort("trips", descending=True)
    .collect())
print(f"polars: {time.perf_counter() - start:.2f} s")
print(res)
start = time.perf_counter()
rel = duckdb.sql(f"""
    SELECT payment_type, COUNT(*) AS trips, ROUND(AVG(tip_amount), 2) AS avg_tip
    FROM '{FILE}'
    WHERE fare_amount > 0
    GROUP BY payment_type
    ORDER BY trips DESC
""")
rows = rel.fetchall()
print(f"duckdb: {time.perf_counter() - start:.2f} s")
rel.show()