from pyspark.sql import functions as F, Window


def latest(df, key, order_col):
    w = Window.partitionBy(key).orderBy(F.col(order_col).desc())
    return df.withColumn("_rn", F.row_number().over(w)).where("_rn = 1").drop("_rn")


def clean_customers(customers):
    return (customers
            .dropDuplicates(["customer_id"])
            .withColumn("city", F.coalesce(F.col("city"), F.lit("Unknown"))))


def clean_orders(orders, products):
    o = latest(orders.dropDuplicates(), "order_id", "updated_at")
    o = o.fillna({"customer_id": 0})
    known = products.select("product_id", F.lit(True).alias("_known"))
    o = o.join(F.broadcast(known), "product_id", "left")
    reason = (F.when(F.col("quantity").isNull() | (F.col("quantity") <= 0), "bad quantity")
              .when(F.col("_known").isNull(), "unknown product"))
    o = o.withColumn("reject_reason", reason).drop("_known")
    good = o.where(F.col("reject_reason").isNull()).drop("reject_reason")
    rejected = o.where(F.col("reject_reason").isNotNull())
    return good, rejected