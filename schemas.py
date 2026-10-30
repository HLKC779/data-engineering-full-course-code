from pyspark.sql import types as T

ORDERS = T.StructType([
    T.StructField("order_id", T.LongType()),
    T.StructField("order_ts", T.TimestampType()),
    T.StructField("customer_id", T.IntegerType()),
    T.StructField("product_id", T.StringType()),
    T.StructField("quantity", T.IntegerType()),
    T.StructField("status", T.StringType()),
    T.StructField("updated_at", T.TimestampType()),
])

CUSTOMERS = "customer_id INT, name STRING, city STRING, signup_date DATE"
PRODUCTS = "product_id STRING, name STRING, category STRING, price DOUBLE"