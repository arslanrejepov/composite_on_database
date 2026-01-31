-- Active: 1769823356550@@127.0.0.1@3306@northwind
USE northwind;

SELECT
    c.id AS customer_id,
    c.company,
    COUNT(o.id) AS total_orders
FROM customers c
LEFT JOIN orders o
    ON c.id = o.customer_id
GROUP BY c.id, c.company
ORDER BY total_orders DESC;
