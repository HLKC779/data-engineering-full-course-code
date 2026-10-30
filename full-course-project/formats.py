import time
from pathlib import Path
import pandas as pd

trips = pd.read_parquet("data/nyc/yellow_tripdata_2024-01.parquet").head(500_000)
print("Rows:", len(trips), "Columns:", len(trips.columns))

trips.to_csv("output/trips.csv", index=False)
trips.to_json("output/trips.jsonl", orient="records", lines=True, date_format="iso")
trips.to_parquet("output/trips.parquet", index=False)

for name in ["trips.csv", "trips.jsonl", "trips.parquet"]:
    path = Path("output") / name
    start = time.perf_counter()
    if name.endswith(".csv"):
        back = pd.read_csv(path)
    elif name.endswith(".jsonl"):
        back = pd.read_json(path, lines=True)
    else:
        back = pd.read_parquet(path)
    secs = time.perf_counter() - start
    mb = path.stat().st_size / 1_000_000
    print(f"{name:14} {mb:6.1f} MB  read in {secs:5.2f} s  pickup: {back['tpep_pickup_datetime'].dtype}")