import time
from pyspark.sql import functions as F
from spark_session import get_spark

spark = get_spark("perf")
lake = spark.read.parquet("data/lake/orders")
print("partitions after read:", lake.rdd.getNumPartitions())
spark.conf.set("spark.sql.adaptive.enabled", "true")

for n in [8, 200]:
    spark.conf.set("spark.sql.shuffle.partitions", n)
    per_customer = lake.groupBy("customer_id").agg(F.sum("quantity").alias("units"))
    t = time.perf_counter(); per_customer.write.mode("overwrite").parquet(f"data/demo/per_customer_{n}")
    print(f"shuffle partitions {n}: {per_customer.rdd.getNumPartitions()} partitions, {time.perf_counter() - t:.2f}s")

day = lake.where("order_date = '2026-10-03'")
print("one day:", day.rdd.getNumPartitions(),
      "repartition(4):", day.repartition(4).rdd.getNumPartitions(),
      "coalesce(1):", day.coalesce(1).rdd.getNumPartitions())

(lake.repartition("order_date")
 .write.mode("overwrite").partitionBy("order_date").parquet("data/lake/orders_compact"))