from spark_session import get_spark

spark = get_spark("read_files")

orders = spark.read.csv("data/raw/orders", header=True, inferSchema=True)
orders.printSchema()
print("orders rows:", orders.count())
orders.show(3)

products = spark.read.json("data/raw/products.jsonl")
products.printSchema()
products.show(3, truncate=False)
customers = spark.read.option("header", True).csv("data/raw/customers.csv")
print("customers rows:", customers.count())

orders.write.mode("overwrite").parquet("data/demo/orders_parquet")
back = spark.read.parquet("data/demo/orders_parquet")
print("parquet rows:", back.count())
back.printSchema()