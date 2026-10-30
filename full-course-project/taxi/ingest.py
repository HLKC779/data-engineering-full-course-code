import sys
from pathlib import Path

import duckdb

HERE = Path(__file__).parent
DATA = HERE.parent / "data" / "nyc"

con = duckdb.connect(str(HERE / "taxi.duckdb"))
con.execute("""
    CREATE TABLE IF NOT EXISTS raw_trips AS
    SELECT *, '' AS source_file
    FROM read_parquet(?) LIMIT 0
""", [str(DATA / f"yellow_tripdata_{sys.argv[1]}.parquet")])

for month in sys.argv[1:]:
    name = f"yellow_tripdata_{month}.parquet"
    con.execute("BEGIN")
    con.execute("DELETE FROM raw_trips WHERE source_file = ?", [name])
    con.execute("INSERT INTO raw_trips SELECT *, ? FROM read_parquet(?)", [name, str(DATA / name)])
    con.execute("COMMIT")
    n = con.execute("SELECT COUNT(*) FROM raw_trips WHERE source_file = ?", [name]).fetchone()[0]
    print(f"{name}: {n:,} rows")

total = con.execute("SELECT COUNT(*) FROM raw_trips").fetchone()[0]
print(f"raw_trips now has {total:,} rows")