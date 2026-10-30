from spark_session import get_spark

spark = get_spark("explore_star")
for t in ["fact_sales", "dim_customer", "dim_product", "dim_date"]:
    spark.read.parquet(f"data/warehouse/{t}").createOrReplaceTempView(t)
spark.sql("""
SELECT d.day_name, d.is_weekend, COUNT(*) AS orders, ROUND(SUM(f.revenue)) AS revenue
FROM fact_sales f JOIN dim_date d ON f.date_key = d.date_key
GROUP BY d.day_name, d.is_weekend ORDER BY revenue DESC
""").show()