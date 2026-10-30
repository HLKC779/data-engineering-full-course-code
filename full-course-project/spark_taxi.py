from pyspark.sql import SparkSession
from pyspark.sql import functions as F

spark = (
    SparkSession.builder.appName("taxi").master("local[*]")
    .config("spark.ui.showConsoleProgress", "false")
    .getOrCreate()
)
spark.sparkContext.setLogLevel("ERROR")

trips = spark.read.parquet("data/nyc/yellow_tripdata_2024-01.parquet")
print("partitions:", trips.rdd.getNumPartitions())
clean = (
    trips.where((F.col("trip_distance") > 0) & (F.col("total_amount") > 0))
    .where(F.col("tpep_pickup_datetime") .between("2024-01-01", "2024-01-31 23:59:59"))
    .withColumn("pickup_date", F.to_date("tpep_pickup_datetime"))
)
daily = (
    clean.groupBy("pickup_date")
    .agg(F.count("*").alias("trips"), F.round(F.sum("total_amount"), 2).alias("revenue"))
    .orderBy("pickup_date")
)
# daily.explain()
daily.show(5)
print("rows:", trips.count(), "clean:", clean.count())

clean.createOrReplaceTempView("trips")
spark.sql(
    "SELECT payment_type, COUNT(*) AS trips, "
    "ROUND(AVG(tip_amount), 2) AS avg_tip "
    "FROM trips GROUP BY payment_type ORDER BY trips DESC"
).show()

clean.write.mode("overwrite").partitionBy("pickup_date").parquet("output/trips_by_day")
spark.stop()