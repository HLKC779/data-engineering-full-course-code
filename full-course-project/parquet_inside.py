import time
import pandas as pd
import pyarrow.parquet as pq

start = time.perf_counter()
fares = pd.read_parquet("output/trips.parquet", columns=["fare_amount"])
print(f"One column: {time.perf_counter() - start:.3f} s")

pf = pq.ParquetFile("output/trips.parquet")
print(pf.schema_arrow)
print("Row groups:", pf.metadata.num_row_groups)
stats = pf.metadata.row_group(0).column(1).statistics
print("pickup min:", stats.min, "max:", stats.max)