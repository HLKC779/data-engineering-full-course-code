DROP TABLE IF EXISTS flat_sales;
CREATE TABLE flat_sales AS
SELECT o.order_id, o.order_date, c.customer_id,
    c.name AS customer_name, c.email, c.country,
    p.name AS product_name, p.category, i.quantity, i.unit_price
FROM order_items AS i
JOIN orders_clean AS o ON o.order_id = i.order_id
JOIN customers AS c ON c.customer_id = o.customer_id
JOIN products AS p ON p.product_id = i.product_id;

SELECT customer_name, email, COUNT(*) AS copies
FROM flat_sales WHERE customer_id = 27
GROUP BY customer_name, email;

UPDATE flat_sales SET email = 'new.address@example.com'
WHERE order_id = (SELECT MIN(order_id) FROM flat_sales WHERE customer_id = 27);

SELECT email, COUNT(*) AS rows_with_it
FROM flat_sales WHERE customer_id = 27
GROUP BY email;