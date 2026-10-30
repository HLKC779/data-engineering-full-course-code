SELECT o.order_id, o.customer_id, c.name, o.amount
FROM orders AS o
JOIN customers AS c ON o.customer_id = c.customer_id
ORDER BY o.order_id LIMIT 5;

SELECT COUNT(*) AS joined_rows
FROM orders AS o
JOIN customers AS c ON o.customer_id = c.customer_id;

SELECT o.order_id, o.customer_id
FROM orders AS o
LEFT JOIN customers AS c ON o.customer_id = c.customer_id
WHERE c.customer_id IS NULL;

SELECT COUNT(*) AS never_ordered
FROM customers AS c
LEFT JOIN orders AS o ON o.customer_id = c.customer_id
WHERE o.order_id IS NULL;

SELECT ROUND(SUM(amount), 2) AS total FROM orders;

SELECT ROUND(SUM(o.amount), 2) AS total
FROM orders AS o
JOIN order_items AS i ON o.order_id = i.order_id;