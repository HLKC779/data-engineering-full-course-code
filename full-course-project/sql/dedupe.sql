DROP TABLE IF EXISTS orders_clean;
CREATE TABLE orders_clean AS
WITH ranked AS (
    SELECT *, ROW_NUMBER() OVER (
        PARTITION BY order_id ORDER BY order_id
    ) AS rn
    FROM orders
)
SELECT order_id, customer_id, order_date, status, amount
FROM ranked
WHERE rn = 1;

SELECT (SELECT COUNT(*) FROM orders) AS raw_rows,
    (SELECT COUNT(*) FROM orders_clean) AS clean_rows;