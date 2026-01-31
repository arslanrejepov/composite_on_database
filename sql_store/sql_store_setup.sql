-- Active: 1769823356550@@127.0.0.1@3306@mysql
/* ===============================
   RESET EVERYTHING (SAFE)
================================ */
DROP DATABASE IF EXISTS sql_store;

/* ===============================
   CREATE DATABASE
================================ */
CREATE DATABASE sql_store;
USE sql_store;

/* ===============================
   CUSTOMERS TABLE
================================ */
CREATE TABLE customers (
    customer_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    birth_date DATE,
    phone VARCHAR(20),
    address VARCHAR(100),
    city VARCHAR(50),
    state VARCHAR(50),
    points INT DEFAULT 0
);

/* ===============================
   PRODUCTS TABLE
================================ */
CREATE TABLE products (
    product_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    quantity_in_stock INT NOT NULL,
    unit_price DECIMAL(6,2) NOT NULL
);

/* ===============================
   SHIPPERS TABLE
================================ */
CREATE TABLE shippers (
    shipper_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL
);

/* ===============================
   ORDERS TABLE
================================ */
CREATE TABLE orders (
    order_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT NOT NULL,
    order_date DATE NOT NULL,
    status TINYINT NOT NULL,
    shipped_date DATE,
    shipper_id INT,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY (shipper_id) REFERENCES shippers(shipper_id)
);

/* ===============================
   ORDER ITEMS TABLE
================================ */
CREATE TABLE order_items (
    order_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL,
    unit_price DECIMAL(6,2) NOT NULL,
    PRIMARY KEY (order_id, product_id),
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

/* ===============================
   INSERT CUSTOMERS
================================ */
INSERT INTO customers
(first_name, last_name, birth_date, phone, address, city, state, points)
VALUES
('John', 'Doe', '1985-02-15', '555-1111', '123 Main St', 'New York', 'NY', 1200),
('Jane', 'Smith', '1990-07-20', '555-2222', '456 Park Ave', 'Chicago', 'IL', 3500),
('Mike', 'Brown', '1978-11-30', '555-3333', '789 Oak St', 'Dallas', 'TX', 2200),
('Sara', 'Wilson', '1995-04-10', '555-4444', '321 Pine St', 'Seattle', 'WA', 800),
('Alex', 'Green', '1988-09-05', '555-5555', '654 Elm St', 'Boston', 'MA', 4100);

/* ===============================
   INSERT PRODUCTS
================================ */
INSERT INTO products (name, quantity_in_stock, unit_price)
VALUES
('Keyboard', 49, 39.99),
('Mouse', 38, 19.99),
('Monitor', 12, 179.99),
('USB Cable', 100, 9.99),
('Laptop Stand', 25, 59.99);

/* ===============================
   INSERT SHIPPERS
================================ */
INSERT INTO shippers (name)
VALUES
('UPS'),
('FedEx'),
('DHL');

/* ===============================
   INSERT ORDERS
================================ */
INSERT INTO orders
(customer_id, order_date, status, shipped_date, shipper_id)
VALUES
(1, '2024-01-10', 1, '2024-01-12', 1),
(2, '2024-01-15', 1, '2024-01-17', 2),
(3, '2024-02-01', 2, NULL, NULL),
(5, '2024-02-10', 1, '2024-02-12', 3);

/* ===============================
   INSERT ORDER ITEMS
================================ */
INSERT INTO order_items
(order_id, product_id, quantity, unit_price)
VALUES
(1, 1, 2, 39.99),
(1, 2, 1, 19.99),
(2, 3, 1, 179.99),
(3, 4, 5, 9.99),
(4, 5, 1, 59.99);

/* ===============================
   TEST QUERIES (MOSH STYLE)
================================ */

-- Basic SELECT
SELECT customer_id, first_name, last_name, points
FROM customers
ORDER BY points DESC;

-- WHERE
SELECT *
FROM customers
WHERE points > 2000;

-- JOIN
SELECT
    o.order_id,
    c.first_name,
    c.last_name,
    o.order_date
FROM orders o
JOIN customers c
    ON o.customer_id = c.customer_id;

-- ORDER ITEMS TOTAL
SELECT
    order_id,
    SUM(quantity * unit_price) AS total_price
FROM order_items
GROUP BY order_id;
