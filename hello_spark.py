from pyspark.sql import SparkSession

spark = SparkSession.builder.master("local[*]").getOrCreate()
print("Spark version:", spark.version)
print("Cores:", spark.sparkContext.defaultParallelism)
df = spark.range(1, 1_000_001)
print("Sum:", df.selectExpr("sum(id)").first()[0])
spark.stop()