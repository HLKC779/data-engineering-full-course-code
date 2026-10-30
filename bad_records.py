import re
from pyspark.sql import types as T
from spark_session import get_spark
from schemas import ORDERS

spark = get_spark("bad_records")
with_bad = T.StructType(ORDERS.fields + [T.StructField("_corrupt", T.StringType())])
df = spark.read.csv("data/bad_orders.csv", header=True, schema=with_bad, columnNameOfCorruptRecord="_corrupt")
df.show()
df.cache()
df.where(df._corrupt.isNotNull()).select("order_id", "_corrupt").show(truncate=False)
try:
    spark.read.csv("data/bad_orders.csv", header=True, schema=ORDERS, mode="FAILFAST").collect()
except Exception as e:
    print("FAILFAST stopped the job:", re.search(r"\[(MALFORMED\w+)", str(e)).group(1))