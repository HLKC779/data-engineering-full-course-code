from spark_session import get_spark

spark = get_spark("read_lake")
lake = spark.read.parquet("data/lake/orders")
lake.printSchema()
one_day = lake.where("order_date = '2026-10-03' AND quantity >= 3")
print("one day, large orders:", one_day.count())
one_day.explain()