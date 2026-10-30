import duckdb

CHECKS = {
    "order_id is unique":
        "SELECT order_id FROM orders GROUP BY order_id HAVING COUNT(*) > 1",
    "amount is present":
        "SELECT order_id FROM orders WHERE amount IS NULL",
    "amount is not negative":
        "SELECT order_id FROM orders WHERE amount < 0",
    "status is valid":
        "SELECT order_id FROM orders WHERE status NOT IN ('completed', 'cancelled', 'refunded')",
    "customer exists":
        "SELECT o.order_id FROM orders AS o LEFT JOIN customers AS c "
        "USING (customer_id) WHERE c.customer_id IS NULL",
}


def run_checks(con):
    failed = 0
    for name, sql in CHECKS.items():
        bad = con.sql(sql).fetchall()
        status = "PASS" if not bad else f"FAIL ({len(bad)} rows)"
        print(f"{name:24} {status}")
        failed += bool(bad)
    return failed


if __name__ == "__main__":
    con = duckdb.connect()
    con.sql("CREATE VIEW orders AS SELECT * FROM read_csv('data/orders.csv')")
    con.sql("CREATE VIEW customers AS SELECT * FROM read_csv('data/customers.csv')")
    failed = run_checks(con)
    print(f"{failed} check(s) failed")
    raise SystemExit(1 if failed else 0)