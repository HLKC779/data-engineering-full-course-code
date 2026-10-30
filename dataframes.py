from spark_session import get_spark

spark = get_spark("dataframes")
rows = [
    (1, "Lahore", "Electronics", 120.5),
    (2, "Austin", "Books", 18.0),
    (3, "Berlin", "Home", 64.25),
    (4, "Lahore", "Books", 22.0),
]
df = spark.createDataFrame(rows, ["order_id", "city", "category", "amount"])
df.show()
df.printSchema()
print("rows:", df.count(), "columns:", df.columns)

schema = "order_id INT, city STRING, category STRING, amount DOUBLE"
df2 = spark.createDataFrame(rows, schema)
df2.printSchema()
print("partitions:", df2.rdd.getNumPartitions())
df2.where(df2.amount > 50).show()