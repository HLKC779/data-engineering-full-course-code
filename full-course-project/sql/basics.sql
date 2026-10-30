SELECT * FROM products LIMIT 5;

SELECT name, unit_price
FROM products
WHERE category = 'tea'
ORDER BY unit_price DESC;

SELECT COUNT(*) AS orders,
    MIN(order_date) AS first_day,
    MAX(order_date) AS last_day
FROM orders;

SELECT DISTINCT status FROM orders;

SELECT order_id, status FROM orders WHERE amount IS NULL;