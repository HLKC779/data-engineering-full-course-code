from pyspark.sql import functions as F
from spark_session import get_spark
import sources

spark = get_spark("nulls_dupes")
orders = sources.orders(spark)
orders.select([F.sum(F.col(c).isNull().cast("int")).alias(c) for c in orders.columns]).show()
print("rows:", orders.count(), "distinct rows:", orders.distinct().count(),
      "distinct order ids:", orders.select("order_id").distinct().count())

from cleaning import clean_orders, clean_customers
good, rejected = clean_orders(orders, sources.products(spark))
print("good:", good.count(), "unique:", good.select("order_id").distinct().count())
rejected.groupBy("reject_reason").count().show()
good.groupBy("status").count().orderBy("status").show()
print("customers:", clean_customers(sources.customers(spark)).count())