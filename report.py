from spark_session import get_spark

W = "data/warehouse"
spark = get_spark("report")
daily = spark.read.parquet(f"{W}/agg_daily").orderBy("date").collect()
top = spark.read.parquet(f"{W}/agg_top_products").orderBy("revenue", ascending=False).limit(5).collect()
cities = spark.read.parquet(f"{W}/agg_city_category").groupBy("city").sum("revenue") \
    .withColumnRenamed("sum(revenue)", "revenue").orderBy("revenue", ascending=False).collect()

total = sum(r.revenue for r in daily)
lines = ["# Daily sales report", "",
         f"Days: {daily[0].date} to {daily[-1].date}  ", f"Orders: {sum(r.orders for r in daily):,}  ",
         f"Revenue: ${total:,.2f}", "", "## Top 5 products", ""]
lines += [f"{i}. {r.name}: ${r.revenue:,.2f} ({r.units} units)" for i, r in enumerate(top, 1)]
lines += ["", "## Revenue by city", ""] + [f"- {r.city}: ${r.revenue:,.2f}" for r in cities]
open("report.md", "w").write("\n".join(lines) + "\n")
print("report.md written:", len(lines), "lines")