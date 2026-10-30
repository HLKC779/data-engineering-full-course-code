from pyspark.sql import functions as F, Window
from spark_session import get_spark
import sources

spark = get_spark("windows")
orders = sources.orders(spark).where("quantity > 0 AND customer_id IS NOT NULL").dropDuplicates()

by_customer = Window.partitionBy("customer_id").orderBy("order_ts")
numbered = (orders
            .withColumn("nth", F.row_number().over(by_customer))
            .withColumn("prev_ts", F.lag("order_ts").over(by_customer))
            .withColumn("gap_h", F.round((F.col("order_ts").cast("long") - F.col("prev_ts").cast("long")) / 3600, 1)))
numbered.where("customer_id = 7").select("customer_id", "order_ts", "nth", "gap_h").show(4)
firsts = numbered.where("nth = 1")
print("customers with a first order:", firsts.count())

sales = (orders.join(F.broadcast(sources.products(spark)), "product_id")
         .withColumn("revenue", F.col("quantity") * F.col("price")))
daily = sales.groupBy(F.to_date("order_ts").alias("day")).agg(F.round(F.sum("revenue"), 2).alias("revenue"))
running = Window.orderBy("day").rowsBetween(Window.unboundedPreceding, Window.currentRow)
daily.withColumn("to_date", F.round(F.sum("revenue").over(running), 2)).orderBy("day").show(4)

by_cat = Window.partitionBy("category").orderBy(F.desc("revenue"))
per_product = sales.groupBy("category", "product_id").agg(F.round(F.sum("revenue"), 2).alias("revenue"))
(per_product.withColumn("rank", F.dense_rank().over(by_cat))
             .where("rank <= 2").orderBy("category", "rank").show())