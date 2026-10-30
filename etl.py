"""Daily warehouse build: clean orders lake -> star schema."""
import sys
from pyspark.sql import functions as F
from spark_session import get_spark
from cleaning import clean_customers
from quality import run_checks
import sources

LAKE, W = "data/lake/orders_current", "data/warehouse"


def dim_customer(spark):
    guest = spark.createDataFrame([(0, "Guest", "Unknown", None)], "customer_id INT, name STRING, city STRING, signup_date DATE")
    return clean_customers(sources.customers(spark)).unionByName(guest)


def dim_date(orders):
    span = orders.agg(F.min("order_date").alias("a"), F.max("order_date").alias("b"))
    return (span.select(F.explode(F.sequence("a", "b")).alias("date"))
            .withColumn("date_key", F.date_format("date", "yyyyMMdd").cast("int"))
            .withColumn("day_name", F.date_format("date", "EEEE"))
            .withColumn("is_weekend", F.dayofweek("date").isin(1, 7)))


def fact_sales(orders, products):
    revenue = F.when(F.col("status") == "refunded", 0.0).otherwise(F.round(F.col("quantity") * F.col("price"), 2))
    return (orders.join(F.broadcast(products.select("product_id", "price")), "product_id")
            .withColumn("date_key", F.date_format("order_date", "yyyyMMdd").cast("int"))
            .withColumn("revenue", revenue)
            .select("order_id", "date_key", "customer_id", "product_id", "quantity", F.col("price").alias("unit_price"), "revenue", "status"))


def publish(df, name, partition=None):
    w = df.write.mode("overwrite")
    if partition:
        w = w.partitionBy(partition)
    w.parquet(f"{W}/{name}")
    print(f"published {name}")


if __name__ == "__main__":
    spark = get_spark("etl")
    orders = spark.read.parquet(LAKE).cache()
    products = sources.products(spark)
    if not run_checks(orders, products):
        sys.exit("quality gate failed: nothing published")
    customers = dim_customer(spark)
    fact = fact_sales(orders, products).cache()
    orphans = fact.join(customers, "customer_id", "left_anti").count()
    if orphans:
        sys.exit(f"{orphans} fact rows without a customer")
    publish(customers, "dim_customer")
    publish(products, "dim_product")
    publish(dim_date(orders), "dim_date")
    publish(fact, "fact_sales", partition="date_key")
    print("fact rows:", fact.count(), "revenue:", fact.agg(F.round(F.sum("revenue"), 2)).first()[0])