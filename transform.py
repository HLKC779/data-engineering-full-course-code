from pyspark.sql import functions as F
from spark_session import get_spark
import sources

spark = get_spark("transform")
orders = sources.orders(spark)

orders.select("order_id", "product_id", "quantity", "status").show(3)
paid = orders.filter((F.col("status") == "paid") & (F.col("quantity") > 0))
print("paid orders:", paid.count())
print("bad quantity:", orders.filter("quantity <= 0").count())

enriched = (orders
            .withColumn("order_date", F.to_date("order_ts"))
            .withColumn("hour", F.hour("order_ts"))
            .withColumn("size", F.when(F.col("quantity") >= 3, "large").otherwise("normal"))
            .withColumn("quantity", F.col("quantity").cast("long"))
            .withColumnRenamed("status", "order_status"))
enriched.select("order_id", "order_date", "hour", "quantity", "size", "order_status").show(5)

products = sources.products(spark)
(products
 .withColumn("code", F.concat_ws("-", F.upper(F.substring("category", 1, 3)), "product_id"))
 .withColumn("band", F.expr("CASE WHEN price < 50 THEN 'low' WHEN price < 200 THEN 'mid' ELSE 'high' END"))
 .select("code", "name", "price", "band")
 .show(5))