SET client_min_messages = warning;
CREATE SCHEMA IF NOT EXISTS mart;
DROP TABLE IF EXISTS mart.fct_sales, mart.dim_customer, mart.dim_product, mart.dim_date;

CREATE TABLE mart.dim_customer AS
SELECT customer_id AS customer_key, name, country, signup_date
FROM customers;

CREATE TABLE mart.dim_product AS
SELECT product_id AS product_key, name AS product_name, category
FROM products;

CREATE TABLE mart.dim_date AS
SELECT d::date AS date_key,
    EXTRACT(month FROM d)::int AS month,
    trim(to_char(d, 'Day')) AS weekday,
    EXTRACT(isodow FROM d) >= 6 AS is_weekend
FROM generate_series('2025-01-01'::date, '2025-12-31'::date, interval '1 day') AS d;

CREATE TABLE mart.fct_sales AS
SELECT i.order_id, o.order_date AS date_key,
    o.customer_id AS customer_key, i.product_id AS product_key,
    i.quantity, i.quantity * i.unit_price AS revenue
FROM order_items AS i
JOIN orders AS o ON o.order_id = i.order_id
WHERE o.status = 'completed';

SELECT COUNT(*) AS fact_rows, SUM(revenue) AS revenue FROM mart.fct_sales;