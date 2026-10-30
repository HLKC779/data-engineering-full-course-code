import json
from datetime import date

with open("output/customers.json") as f:
    customers = json.load(f)

first = date.fromisoformat(customers[0]["signup"])
days = (date(2026, 1, 1) - first).days
print(customers[0]["email"], "signed up", days, "days before 2026")