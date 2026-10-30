import json, sys
from pathlib import Path
from pyspark.sql import functions as F
from spark_session import get_spark
from cleaning import clean_orders, latest
import sources

LAKE = "data/lake/orders_current"
STATE = Path("data/state/loaded_files.json")

spark = get_spark("incremental")
spark.conf.set("spark.sql.sources.partitionOverwriteMode", "dynamic")

done = set(json.loads(STATE.read_text())) if STATE.exists() else set()
files = sorted(str(p) for p in Path("data/raw/orders").glob("orders_*.csv"))
new = [f for f in files if f not in done]
print("files:", len(files), "already loaded:", len(done), "new:", len(new))
if not new:
    print("nothing to do")
    sys.exit(0)

batch, rejected = clean_orders(sources.orders(spark, new), sources.products(spark))
batch = batch.withColumn("order_date", F.to_date("order_ts"))
if Path(LAKE).exists():
    dates = [r.order_date for r in batch.select("order_date").distinct().collect()]
    old = spark.read.parquet(LAKE).where(F.col("order_date").isin(dates))
    merged = latest(old.unionByName(batch), "order_id", "updated_at")
else:
    merged = batch
merged = merged.localCheckpoint()
merged.repartition("order_date").write.mode("overwrite").partitionBy("order_date").parquet(LAKE)
STATE.parent.mkdir(parents=True, exist_ok=True)
STATE.write_text(json.dumps(sorted(done | set(new)), indent=1))

lake = spark.read.parquet(LAKE)
print("batch rows:", batch.count(), "lake rows:", lake.count(), "unique:", lake.select("order_id").distinct().count())
lake.groupBy("status").count().orderBy("status").show()