from schemas import ORDERS, CUSTOMERS, PRODUCTS


def orders(spark, path="data/raw/orders"):
    return spark.read.csv(path, header=True, schema=ORDERS)


def customers(spark):
    return spark.read.csv("data/raw/customers.csv", header=True, schema=CUSTOMERS)


def products(spark):
    return spark.read.schema(PRODUCTS).json("data/raw/products.jsonl")