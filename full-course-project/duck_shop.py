import duckdb

con = duckdb.connect("shop.duckdb")
con.sql("CREATE OR REPLACE TABLE orders AS SELECT * FROM read_csv('data/orders.csv')")
con.sql("DESCRIBE orders").show()
con.sql("""
    COPY (
        SELECT date_trunc('month', order_date) AS month, SUM(amount) AS revenue
        FROM orders WHERE status = 'completed'
        GROUP BY ALL ORDER BY month
    ) TO 'output/monthly_revenue.parquet' (FORMAT parquet)
""")
con.sql("SELECT COUNT(*) AS months FROM 'output/monthly_revenue.parquet'").show()