from spark_session import get_spark
import sources

spark = get_spark("spark_sql")
sources.orders(spark).createOrReplaceTempView("orders")
sources.products(spark).createOrReplaceTempView("products")
sources.customers(spark).createOrReplaceTempView("customers")
spark.sql("SHOW TABLES").show()

city_revenue = spark.sql("""
WITH clean_customers AS (
    SELECT DISTINCT customer_id, city FROM customers
), sales AS (
    SELECT o.customer_id, o.quantity * p.price AS revenue
    FROM orders o JOIN products p ON o.product_id = p.product_id
    WHERE o.quantity > 0 AND o.status <> 'refunded'
)
SELECT c.city, COUNT(*) AS orders, ROUND(SUM(s.revenue), 0) AS revenue
FROM sales s JOIN clean_customers c ON s.customer_id = c.customer_id
GROUP BY c.city
ORDER BY revenue DESC
""")
city_revenue.show()

from pyspark.sql import functions as F
total = city_revenue.agg(F.sum("revenue")).first()[0]
city_revenue.withColumn("share_pct", F.round(F.col("revenue") / total * 100, 1)).show()
spark.sql("SELECT status, COUNT(*) AS n FROM orders GROUP BY status").where("n > 5000").show()

city_revenue.createOrReplaceTempView("city_revenue")
spark.sql("SELECT city FROM city_revenue WHERE revenue > (SELECT AVG(revenue) FROM city_revenue)").show()
spark.sql("SELECT * FROM city_revenue").explain()