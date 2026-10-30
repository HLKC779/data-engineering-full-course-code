WITH RECURSIVE days(day) AS (
    SELECT '2025-01-01'
    UNION ALL
    SELECT date(day, '+1 day') FROM days
    WHERE day < '2025-12-31'
)
SELECT COUNT(*) AS days_in_year,
    SUM(o.order_date IS NULL) AS days_without_orders
FROM days AS d
LEFT JOIN (SELECT DISTINCT order_date FROM orders_clean) AS o
ON o.order_date = d.day;