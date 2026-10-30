import csv
from pathlib import Path

rows = 0
total = 0.0
missing = 0
dupes = 0
seen = set()
clean = []

with open("data/orders.csv", newline="") as f:
    reader = csv.DictReader(f)
    for row in reader:
        rows += 1
        if row["order_id"] in seen:
            dupes += 1
            continue
        seen.add(row["order_id"])
        if row["amount"] == "":
            missing += 1
            continue
        clean.append(row)
        if row["status"] == "completed":
            total += float(row["amount"])

print("Rows:", rows)
print("Duplicates skipped:", dupes)
print("Missing amounts:", missing)
print("Revenue:", round(total, 2))

Path("output").mkdir(exist_ok=True)
with open("output/orders_clean.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=reader.fieldnames)
    writer.writeheader()
    writer.writerows(clean)
print("Clean rows written:", len(clean))