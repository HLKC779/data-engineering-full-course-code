import json

from confluent_kafka import Consumer

consumer = Consumer({
    "bootstrap.servers": "localhost:9092",
    "group.id": "revenue",
    "auto.offset.reset": "earliest",
})
consumer.subscribe(["orders"])

revenue, events, idle = 0.0, 0, 0
while idle < 5:
    msg = consumer.poll(1.0)
    if msg is None:
        if consumer.assignment():
            idle += 1
        continue
    idle = 0
    order = json.loads(msg.value())
    events += 1
    if order["status"] == "completed" and order["amount"]:
        revenue += float(order["amount"])
    print(f"partition {msg.partition()} offset {msg.offset()}: "
        f"order {order['order_id']}, running revenue {revenue:.2f}")

consumer.close()
print(f"{events} events read, no new events for 5 seconds, stopping")