import csv
import json
from datetime import date


def read_rows(path):
    with open(path, newline="") as f:
        for row in csv.DictReader(f):
            yield row


def clean_email(raw):
    return raw.strip().lower()



def parse_date(text):
    return date.fromisoformat(text)



customers = []
for row in read_rows("data/customers.csv"):
    customers.append({
        "id": int(row["customer_id"]),
        "email": clean_email(row["email"]),
        "country": row["country"] or None,
        "signup": parse_date(row["signup_date"]),
    })

print(len(customers), "customers")
print(customers[22])

by_month = {}
for c in customers:
    key = c["signup"].strftime("%Y-%m")
    by_month[key] = by_month.get(key, 0) + 1
for key in sorted(by_month)[-3:]:
    print(key, by_month[key])

with open("output/customers.json", "w") as f:
    json.dump(customers, f, indent=2, default=str)
print("Saved", len(customers), "customers as JSON")