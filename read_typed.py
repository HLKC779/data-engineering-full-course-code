from spark_session import get_spark
from schemas import ORDERS, CUSTOMERS, PRODUCTS

spark = get_spark("read_typed")
orders = spark.read.csv("data/raw/orders", header=True, schema=ORDERS)
customers = spark.read.csv("data/raw/customers.csv", header=True, schema=CUSTOMERS)
products = spark.read.schema(PRODUCTS).json("data/raw/products.jsonl")
orders.printSchema()
customers.printSchema()
print("orders:", orders.count(), "customers:", customers.count(), "products:", products.count())