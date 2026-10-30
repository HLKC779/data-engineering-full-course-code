SELECT order_id, customer_id, order_date,
    ROW_NUMBER() OVER (
        PARTITION BY customer_id
        ORDER BY order_date, order_id
    ) AS nth_order
FROM orders
WHERE customer_id = 7
ORDER BY nth_order LIMIT 5;

SELECT order_id, amount,
    ROW_NUMBER() OVER (ORDER BY amount DESC) AS row_num,
    RANK() OVER (ORDER BY amount DESC) AS rnk,
    DENSE_RANK() OVER (ORDER BY amount DESC) AS dense
FROM orders
WHERE customer_id = 7 AND amount IS NOT NULL
ORDER BY amount DESC LIMIT 6;

SELECT month, revenue,
    ROUND(SUM(revenue) OVER (ORDER BY month), 2) AS running_total,
    ROUND(revenue - LAG(revenue) OVER (ORDER BY month), 2) AS change,
    ROUND(AVG(revenue) OVER (ORDER BY month ROWS BETWEEN 2 PRECEDING AND CURRENT ROW), 1) AS avg_3m
FROM (
    SELECT strftime('%Y-%m', order_date) AS month,
        ROUND(SUM(amount), 2) AS revenue
    FROM orders WHERE status = 'completed'
    GROUP BY month
)
ORDER BY month;

SELECT order_id, customer_id FROM (
    SELECT *, ROW_NUMBER() OVER (PARTITION BY order_id ORDER BY order_id) AS rn
    FROM orders
) WHERE rn > 1;