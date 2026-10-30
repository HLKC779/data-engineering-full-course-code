DROP TABLE IF EXISTS customers;
CREATE TABLE customers (
    customer_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT,
    country TEXT,
    signup_date TEXT
);

DROP TABLE IF EXISTS products;
CREATE TABLE products (
    product_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    category TEXT,
    unit_price REAL
);

DROP TABLE IF EXISTS orders;
CREATE TABLE orders (
    order_id INTEGER,
    customer_id INTEGER,
    order_date TEXT,
    status TEXT,
    amount REAL
);

DROP TABLE IF EXISTS order_items;
CREATE TABLE order_items (
    order_id INTEGER,
    product_id INTEGER,
    quantity INTEGER,
    unit_price REAL
);

.import --csv --skip 1 data/customers.csv customers
.import --csv --skip 1 data/products.csv products
.import --csv --skip 1 data/orders.csv orders
.import --csv --skip 1 data/order_items.csv order_items

UPDATE orders SET amount = NULL WHERE amount = '';
UPDATE customers SET country = NULL WHERE country = '';
UPDATE customers SET email = lower(trim(email));