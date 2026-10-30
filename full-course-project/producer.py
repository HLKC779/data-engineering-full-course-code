import csv
import json
import sys

from confluent_kafka import Producer

producer = Producer({"bootstrap.servers": "localhost:9092"})
start, count = int(sys.argv[1]), int(sys.argv[2])

with open("data/orders.csv", newline="") as f:
    rows = list(csv.DictReader(f))[start:start + count]

for r in rows:
    event = json.dumps(r)
    producer.produce("orders", key=r["customer_id"], value=event)
    print("sent", r["order_id"], r["status"], r["amount"])

producer.flush()
print(f"{len(rows)} events delivered")