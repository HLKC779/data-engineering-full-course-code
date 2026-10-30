from spark_session import get_spark

W = "data/warehouse"
QUERIES = {
    "agg_daily": """SELECT d.date, COUNT(*) AS orders, ROUND(SUM(f.revenue), 2) AS revenue
        FROM fact_sales f JOIN dim_date d USING (date_key) GROUP BY d.date""",
    "agg_city_category": """SELECT c.city, p.category, ROUND(SUM(f.revenue), 2) AS revenue
        FROM fact_sales f JOIN dim_customer c USING (customer_id)
        JOIN dim_product p USING (product_id) GROUP BY c.city, p.category""",
    "agg_top_products": """SELECT p.name, SUM(f.quantity) AS units, ROUND(SUM(f.revenue), 2) AS revenue
        FROM fact_sales f JOIN dim_product p USING (product_id) GROUP BY p.name""",
}

if __name__ == "__main__":
    spark = get_spark("aggregates")
    for t in ["fact_sales", "dim_customer", "dim_product", "dim_date"]:
        spark.read.parquet(f"{W}/{t}").createOrReplaceTempView(t)
    for name, sql in QUERIES.items():
        spark.sql(sql).coalesce(1).write.mode("overwrite").parquet(f"{W}/{name}")
        print("built", name)