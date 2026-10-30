SELECT date_trunc('month', order_date)::date AS month,
       COUNT(*) AS orders,
       SUM(amount) AS revenue
FROM orders
WHERE status = 'completed'
GROUP BY date_trunc('month', order_date)::date
ORDER BY date_trunc('month', order_date)::date DESC
LIMIT 3;

EXPLAIN SELECT * FROM orders WHERE customer_id = 7;
CREATE INDEX IF NOT EXISTS orders_customer_idx ON orders (customer_id);
ANALYZE orders;
EXPLAIN SELECT * FROM orders WHERE customer_id = 7;