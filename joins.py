from pyspark.sql import functions as F
from spark_session import get_spark
import sources

spark = get_spark("joins")
orders = sources.orders(spark)
products = sources.products(spark)
customers = sources.customers(spark)
print("orders:", orders.count())

inner = orders.join(products, "product_id")
left = orders.join(products, "product_id", "left")
anti = orders.join(products, "product_id", "left_anti")
print("inner:", inner.count(), "left:", left.count(), "anti:", anti.count())
anti.groupBy("product_id").count().show()

with_cust = orders.join(customers, "customer_id")
print("orders with a customer:", orders.where("customer_id IS NOT NULL").count(), "joined:", with_cust.count())
dupes = customers.groupBy("customer_id").count().where("count > 1")
print("duplicate customer ids:", dupes.count())
fixed = orders.join(customers.dropDuplicates(["customer_id"]), "customer_id")
print("after dedup:", fixed.count())

spark.conf.set("spark.sql.autoBroadcastJoinThreshold", -1)
orders.join(products, "product_id").explain()
orders.join(F.broadcast(products), "product_id").explain()