from pathlib import Path

import duckdb

con = duckdb.connect(str(Path(__file__).parent / "taxi.duckdb"), read_only=True)

print("Trips and revenue per month")
print(con.sql("""
    SELECT strftime(pickup_date, '%Y-%m') AS month, COUNT(*) AS trips,
    ROUND(SUM(total_amount)) AS revenue
    FROM fct_trips GROUP BY 1 ORDER BY 1
"""))

print("Busiest pickup zones")
print(con.sql("""
    SELECT pickup_borough, pickup_zone, COUNT(*) AS trips
    FROM fct_trips GROUP BY ALL ORDER BY trips DESC LIMIT 5
"""))

print("Credit card tips by hour of day")
print(con.sql("""
    SELECT pickup_hour, COUNT(*) AS trips,
    ROUND(100 * SUM(tip_amount) / SUM(fare_amount), 1) AS tip_pct
    FROM fct_trips WHERE payment_type = 1
    GROUP BY 1 ORDER BY tip_pct DESC LIMIT 5
"""))