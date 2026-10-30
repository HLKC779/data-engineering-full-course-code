WITH customer_totals AS (
    SELECT customer_id, SUM(amount) AS spent
    FROM orders
    WHERE status = 'completed'
    GROUP BY customer_id
),
average AS (
    SELECT AVG(spent) AS avg_spent FROM customer_totals
)
SELECT COUNT(*) AS above_average,
    ROUND(MAX(a.avg_spent), 2) AS avg_spent
FROM customer_totals AS c, average AS a
WHERE c.spent > a.avg_spent;