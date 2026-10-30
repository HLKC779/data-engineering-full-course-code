import time
from pyspark.sql import functions as F, types as T
from spark_session import get_spark

spark = get_spark("udfs")
df = spark.range(3_000_000).withColumn("price", (F.col("id") % 1000) + 0.99)


def band(price):
    if price < 50:
        return "low"
    return "mid" if price < 200 else "high"


band_udf = F.udf(band, T.StringType())
builtin = F.when(F.col("price") < 50, "low").when(F.col("price") < 200, "mid").otherwise("high")

for name, expr in [("python udf", band_udf("price")), ("built-in", builtin)]:
    t = time.perf_counter()
    counts = df.withColumn("band", expr).groupBy("band").count().collect()
    print(f"{name}: {time.perf_counter() - t:.2f}s", sorted((r.band, r["count"]) for r in counts))

df.withColumn("band", band_udf("price")).explain()

@F.udf(returnType=T.StringType())
def initials(name):
    return "".join(w[0] for w in name.split()) if name else None

people = spark.createDataFrame([("Ada Lovelace",), ("Alan Turing",), (None,)], "name STRING")
people.withColumn("initials", initials("name")).show()