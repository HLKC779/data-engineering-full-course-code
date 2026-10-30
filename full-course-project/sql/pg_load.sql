\copy customers FROM 'data/customers.csv' WITH (FORMAT csv, HEADER true)
\copy products FROM 'data/products.csv' WITH (FORMAT csv, HEADER true)
CREATE TEMP TABLE orders_raw (LIKE orders);
\copy orders_raw FROM 'data/orders.csv' WITH (FORMAT csv, HEADER true)
INSERT INTO orders
SELECT DISTINCT ON (order_id) *
FROM orders_raw
WHERE customer_id IN (SELECT customer_id FROM customers)
ORDER BY order_id;
CREATE TEMP TABLE items_raw (LIKE order_items);
\copy items_raw FROM 'data/order_items.csv' WITH (FORMAT csv, HEADER true)
INSERT INTO order_items
SELECT * FROM items_raw
WHERE order_id IN (SELECT order_id FROM orders);
SELECT (SELECT COUNT(*) FROM orders_raw) AS raw_orders,
    (SELECT COUNT(*) FROM orders) AS loaded_orders,
    (SELECT COUNT(*) FROM items_raw) AS raw_items,
    (SELECT COUNT(*) FROM order_items) AS loaded_items;