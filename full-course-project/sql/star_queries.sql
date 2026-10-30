SELECT d.weekday, COUNT(DISTINCT f.order_id) AS orders,
    SUM(f.revenue) AS revenue
FROM mart.fct_sales AS f
JOIN mart.dim_date AS d ON d.date_key = f.date_key
GROUP BY d.weekday ORDER BY revenue DESC;

SELECT c.country, p.category, SUM(f.revenue) AS revenue
FROM mart.fct_sales AS f
JOIN mart.dim_customer AS c ON c.customer_key = f.customer_key
JOIN mart.dim_product AS p ON p.product_key = f.product_key
GROUP BY c.country, p.category ORDER BY revenue DESC LIMIT 5;