import csv
import sys
import psycopg

path = sys.argv[1]
with open(path, newline="") as f:
    rows = list(csv.DictReader(f))

with psycopg.connect() as con:
    con.execute("""
        CREATE TABLE IF NOT EXISTS orders_inc (
            order_id INTEGER PRIMARY KEY, customer_id INTEGER, order_date DATE,
            status TEXT, amount NUMERIC(10, 2))
    """)
    con.execute("CREATE TABLE IF NOT EXISTS load_log "
            "(file TEXT PRIMARY KEY, loaded_at TIMESTAMPTZ DEFAULT now())")
    if con.execute("SELECT 1 FROM load_log WHERE file = %s", (path,)).fetchone():
        print(f"{path} already loaded, skipping")
        sys.exit(0)
    for r in rows:
        con.execute(
            "INSERT INTO orders_inc VALUES (%s, %s, %s, %s, %s) "
            "ON CONFLICT (order_id) DO UPDATE "
            "SET status = EXCLUDED.status, amount = EXCLUDED.amount",
            (r["order_id"], r["customer_id"], r["order_date"], r["status"], r["amount"]))
    con.execute("INSERT INTO load_log (file) VALUES (%s)", (path,))
    total = con.execute("SELECT COUNT(*) FROM orders_inc").fetchone()[0]
print(f"Loaded {len(rows)} rows from {path}, table now has {total} rows")