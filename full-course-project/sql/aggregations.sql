SELECT status,
    COUNT(*) AS orders,
    COUNT(amount) AS with_amount,
    ROUND(SUM(amount), 2) AS revenue
FROM orders
GROUP BY status;

SELECT strftime('%Y-%m', order_date) AS month,
    COUNT(*) AS orders,
    ROUND(SUM(amount), 2) AS revenue
FROM orders
WHERE status = 'completed'
GROUP BY month
ORDER BY month;

SELECT customer_id, COUNT(*) AS orders,
    ROUND(SUM(amount), 2) AS spent
FROM orders
WHERE status = 'completed'
GROUP BY customer_id
HAVING COUNT(*) >= 20
ORDER BY spent DESC;

SELECT CASE
    WHEN amount < 10 THEN 'small'
    WHEN amount < 30 THEN 'medium'
    ELSE 'large'
END AS size,
    COUNT(*) AS orders
FROM orders
WHERE amount IS NOT NULL
GROUP BY size;

SELECT p.category,
    SUM(i.quantity) AS units,
    ROUND(SUM(i.quantity * i.unit_price), 2) AS revenue
FROM order_items AS i
JOIN products AS p ON p.product_id = i.product_id
JOIN orders AS o ON o.order_id = i.order_id
WHERE o.status = 'completed'
GROUP BY p.category
ORDER BY revenue DESC;