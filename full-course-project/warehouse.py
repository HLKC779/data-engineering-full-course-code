import time

import duckdb

con = duckdb.connect()
TRIPS = "read_parquet('output/trips_by_day/*/*.parquet', hive_partitioning = true)"


def run(title, where=""):
    sql = f"SELECT COUNT(*), ROUND(SUM(total_amount), 2) FROM {TRIPS} {where}"
    start = time.perf_counter()
    trips, revenue = con.sql(sql).fetchone()
    ms = (time.perf_counter() - start) * 1000
    plan = con.sql("EXPLAIN ANALYZE " + sql).fetchone()[1]
    files = [line.strip(" \u2502") for line in plan.split("\n") if "Scanning Files" in line]
    print(f"{title}: {trips} trips, {revenue} dollars, {ms:.0f} ms, {files[0] if files else 'all files'}")


run("whole month")
run("one week", "WHERE pickup_date BETWEEN '2024-01-08' AND '2024-01-14'")
run("one day", "WHERE pickup_date = '2024-01-15'")