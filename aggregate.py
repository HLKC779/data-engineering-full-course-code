from pyspark.sql import functions as F
from spark_session import get_spark
import sources

spark = get_spark("aggregate")
orders = sources.orders(spark).filter("quantity > 0")

orders.groupBy("status").count().orderBy(F.desc("count")).show()

daily = (orders
         .groupBy(F.to_date("order_ts").alias("day"))
         .agg(F.count("*").alias("orders"),
              F.sum("quantity").alias("units"),
              F.countDistinct("customer_id").alias("customers"),
              F.round(F.avg("quantity"), 2).alias("avg_qty"))
         .orderBy("day"))
daily.show(5)

(orders.groupBy(F.to_date("order_ts").alias("day"))
       .pivot("status", ["paid", "shipped", "refunded"])
       .count().orderBy("day").show(3))

top = (orders.groupBy("product_id")
       .agg(F.sum("quantity").alias("units"))
       .orderBy(F.desc("units"))
       .limit(5))
top.show()
print("distinct customers:", orders.select("customer_id").distinct().count(),
      "approx:", orders.agg(F.approx_count_distinct("customer_id")).first()[0])