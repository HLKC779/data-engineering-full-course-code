SET client_min_messages = warning;
DROP TABLE IF EXISTS order_items, orders, products, customers;

CREATE TABLE customers (
    customer_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    country CHAR(2),
    signup_date DATE NOT NULL
);
CREATE TABLE products (
    product_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    category TEXT NOT NULL,
    unit_price NUMERIC(10, 2) NOT NULL CHECK (unit_price >= 0)
);
CREATE TABLE orders (
    order_id INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL REFERENCES customers,
    order_date DATE NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('completed', 'cancelled', 'refunded')),
    amount NUMERIC(10, 2) CHECK (amount >= 0)
);
CREATE TABLE order_items (
    order_id INTEGER NOT NULL REFERENCES orders,
    product_id INTEGER NOT NULL REFERENCES products,
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    unit_price NUMERIC(10, 2) NOT NULL,
    PRIMARY KEY (order_id, product_id)
);