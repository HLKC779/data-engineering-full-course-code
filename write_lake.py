from pyspark.sql import functions as F
from spark_session import get_spark
from cleaning import clean_orders
import sources

spark = get_spark("write_lake")
good, rejected = clean_orders(sources.orders(spark), sources.products(spark))
good = good.withColumn("order_date", F.to_date("order_ts"))

(good.write
 .mode("overwrite")
 .partitionBy("order_date")
 .parquet("data/lake/orders"))
rejected.write.mode("overwrite").parquet("data/lake/rejected_orders")
print("written:", good.count(), "rejected:", rejected.count())