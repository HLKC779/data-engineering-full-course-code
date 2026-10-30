import time
from pyspark.sql import functions as F
from spark_session import get_spark
import sources

spark = get_spark("lazy")
orders, products = sources.orders(spark), sources.products(spark)
t = time.perf_counter()
sales = (orders
         .where("quantity > 0")
         .join(F.broadcast(sources.products(spark)), "product_id")
         .withColumn("revenue", F.col("quantity") * F.col("price"))
         .groupBy("category").agg(F.round(F.sum("revenue")).alias("revenue")))
print(f"building the plan: {time.perf_counter() - t:.3f}s")
t = time.perf_counter()
rows = sales.collect()
print(f"running it: {time.perf_counter() - t:.3f}s", len(rows), "categories")
sales.explain("extended")

clean = sources.orders(spark).where("quantity > 0").dropDuplicates()
for label in ["no cache, 1st", "no cache, 2nd"]:
    t = time.perf_counter(); n = clean.count()
    print(f"{label}: {time.perf_counter() - t:.2f}s", n)
clean.cache()
for label in ["cached, 1st", "cached, 2nd"]:
    t = time.perf_counter(); n = clean.count()
    print(f"{label}: {time.perf_counter() - t:.2f}s", n)
clean.unpersist()