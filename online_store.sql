CREATE DATABASE OnlineStoreDB_046;


USE OnlineStoreDB_046;

CREATE TABLE Categories_046 (
    category_id INT AUTO_INCREMENT PRIMARY KEY,
    category_name VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE Suppliers_046 (
    supplier_id INT AUTO_INCREMENT PRIMARY KEY,
    company_name VARCHAR(150) NOT NULL,
    contact_person VARCHAR(100),
    phone VARCHAR(20),
    email VARCHAR(100),
    address VARCHAR(255)
);

CREATE TABLE Products_046 (
    product_id INT AUTO_INCREMENT PRIMARY KEY,
    product_name VARCHAR(150) NOT NULL,
    description TEXT,
    selling_price DECIMAL(10,2) NOT NULL,
    purchase_price DECIMAL(10,2) NOT NULL,
    status ENUM('Available','Unavailable') DEFAULT 'Available',
    member_discount DECIMAL(5,2) DEFAULT 0.00,

    category_id INT NOT NULL,
    supplier_id INT NOT NULL,

    CONSTRAINT fk_product_category
        FOREIGN KEY (category_id)
        REFERENCES Categories_046(category_id),

    CONSTRAINT fk_product_supplier
        FOREIGN KEY (supplier_id)
        REFERENCES Suppliers_046(supplier_id)
);


CREATE TABLE Inventory_046 (
    inventory_id INT AUTO_INCREMENT PRIMARY KEY,
    stock_quantity INT NOT NULL DEFAULT 0,
    reorder_level INT NOT NULL DEFAULT 10,
    last_updated DATETIME DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,

    product_id INT NOT NULL UNIQUE,

    CONSTRAINT fk_inventory_product
        FOREIGN KEY (product_id)
        REFERENCES Products_046(product_id)
);

CREATE TABLE Customers_046 (
    customer_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE,
    phone VARCHAR(20),
    address VARCHAR(255),
    membership_level ENUM('Regular','Silver','Gold','VIP')
        DEFAULT 'Regular',
    total_points INT DEFAULT 0
);

CREATE TABLE Orders_046 (
    order_id INT AUTO_INCREMENT PRIMARY KEY,
    order_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    status ENUM('Pending','Processing','Completed','Cancelled')
        DEFAULT 'Pending',
    total_amount DECIMAL(10,2) NOT NULL,

    customer_id INT NOT NULL,

    CONSTRAINT fk_order_customer
        FOREIGN KEY (customer_id)
        REFERENCES Customers_046(customer_id)
);


CREATE TABLE Order_Item_046 (
    order_item_id INT AUTO_INCREMENT PRIMARY KEY,
    quantity INT NOT NULL,
    unit_price DECIMAL(10,2) NOT NULL,

    order_id INT NOT NULL,
    product_id INT NOT NULL,

    CONSTRAINT fk_item_order
        FOREIGN KEY (order_id)
        REFERENCES Orders_046(order_id),

    CONSTRAINT fk_item_product
        FOREIGN KEY (product_id)
        REFERENCES Products_046(product_id)
);

CREATE TABLE Payments_046 (
    payment_id INT AUTO_INCREMENT PRIMARY KEY,
    payment_date DATETIME DEFAULT CURRENT_TIMESTAMP,

    payment_method ENUM(
        'Cash',
        'Credit Card',
        'Debit Card',
        'Online Payment'
    ) NOT NULL,

    payment_status ENUM(
        'Pending',
        'Paid',
        'Failed',
        'Refunded'
    ) DEFAULT 'Pending',

    amount DECIMAL(10,2) NOT NULL,

    order_id INT NOT NULL UNIQUE,

    CONSTRAINT fk_payment_order
        FOREIGN KEY (order_id)
        REFERENCES Orders_046(order_id)
);

CREATE TABLE Users_046 (
    user_id INT AUTO_INCREMENT PRIMARY KEY,

    username VARCHAR(50) NOT NULL UNIQUE,

    password VARCHAR(255) NOT NULL,

    role ENUM(
        'Manager',
        'Cashier',
        'Inventory Clerk'
    ) NOT NULL
);


INSERT INTO Categories_046 (category_name) VALUES
('Electronics'),
('Clothing'),
('Books'),
('Home & Kitchen'),
('Sports');

INSERT INTO Suppliers_046
(company_name, contact_person, phone, email, address)
VALUES
('Tech World Ltd.', 'John Smith', '1234567890', 'john@techworld.com', 'New York'),
('Fashion Hub', 'Emma Brown', '2233445566', 'emma@fashionhub.com', 'Los Angeles'),
('Book House', 'David Wilson', '3344556677', 'david@bookhouse.com', 'Chicago'),
('Home Supplies Inc.', 'Sophia Davis', '4455667788', 'sophia@homesupplies.com', 'Houston'),
('Sport Zone', 'Michael Lee', '5566778899', 'michael@sportzone.com', 'Miami');

INSERT INTO Customers_046
(name, email, phone, address, membership_level, total_points)
VALUES
('Alice Johnson', 'alice@gmail.com', '1111111111', 'California', 'Gold', 250),
('Bob Williams', 'bob@gmail.com', '2222222222', 'Texas', 'Regular', 50),
('Charlie Brown', 'charlie@gmail.com', '3333333333', 'Florida', 'Silver', 120),
('Diana Miller', 'diana@gmail.com', '4444444444', 'Nevada', 'VIP', 600),
('Ethan Davis', 'ethan@gmail.com', '5555555555', 'Arizona', 'Regular', 0);

INSERT INTO Users_046
(username, password, role)
VALUES
('manager1', 'manager123', 'Manager'),
('cashier1', 'cashier123', 'Cashier'),
('inventory1', 'inventory123', 'Inventory Clerk');

INSERT INTO Products_046
(product_name, description, selling_price, purchase_price,
status, member_discount, category_id, supplier_id)
VALUES
('Laptop', '15-inch gaming laptop', 1200.00, 950.00, 'Available', 10.00, 1, 1),
('Smartphone', 'Android smartphone', 800.00, 650.00, 'Available', 5.00, 1, 1),
('T-Shirt', 'Cotton T-Shirt', 25.00, 15.00, 'Available', 0.00, 2, 2),
('Database Book', 'Learning SQL', 50.00, 30.00, 'Available', 15.00, 3, 3),
('Football', 'Professional football', 40.00, 22.00, 'Available', 8.00, 5, 5);

INSERT INTO Inventory_046
(stock_quantity, reorder_level, product_id)
VALUES
(50,10,1),
(80,15,2),
(120,20,3),
(40,10,4),
(70,15,5);

INSERT INTO Orders_046
(order_date, status, total_amount, customer_id)
VALUES
('2026-06-20','Completed',1250.00,1),
('2026-06-21','Pending',25.00,2),
('2026-06-22','Completed',90.00,3),
('2026-06-23','Processing',800.00,4),
('2026-06-24','Cancelled',40.00,5);

INSERT INTO Order_Item_046
(quantity, unit_price, order_id, product_id)
VALUES
(1,1200.00,1,1),
(1,50.00,1,4),
(1,25.00,2,3),
(1,50.00,3,4),
(1,40.00,3,5),
(1,800.00,4,2),
(1,40.00,5,5);

INSERT INTO Payments_046
(payment_date, payment_method, payment_status, amount, order_id)
VALUES
('2026-06-20','Credit Card','Paid',1250.00,1),
('2026-06-21','Cash','Pending',25.00,2),
('2026-06-22','Debit Card','Paid',90.00,3),
('2026-06-23','Online Payment','Pending',800.00,4),
('2026-06-24','Cash','Refunded',40.00,5);

CREATE TABLE Points_Record_046 (
    record_id INT AUTO_INCREMENT PRIMARY KEY,

    points_earned INT NOT NULL,

    earned_date DATETIME DEFAULT CURRENT_TIMESTAMP,

    customer_id INT NOT NULL,

    order_id INT NOT NULL UNIQUE,

    CONSTRAINT fk_points_customer
        FOREIGN KEY (customer_id)
        REFERENCES Customers_046(customer_id),

    CONSTRAINT fk_points_order
        FOREIGN KEY (order_id)
        REFERENCES Orders_046(order_id)
);

INSERT INTO Points_Record_046
(points_earned, earned_date, customer_id, order_id)
VALUES
(1250,'2026-06-20',1,1),
(90,'2026-06-22',3,3);





SELECT * FROM Categories_046;
SELECT * FROM Suppliers_046;
SELECT * FROM Customers_046;
SELECT * FROM Users_046;
SELECT * FROM Products_046;
SELECT * FROM Inventory_046;
SELECT * FROM Orders_046;
SELECT * FROM Order_Item_046;
SELECT * FROM Payments_046;
SELECT * FROM Points_Record_046;

CREATE INDEX idx_product_name_046
ON Products_046(product_name);

CREATE INDEX idx_customer_email_046
ON Customers_046(email);

CREATE INDEX idx_order_date_046
ON Orders_046(order_date);

CREATE INDEX idx_payment_status_046
ON Payments_046(payment_status);

CREATE INDEX idx_orderitem_product_046
ON Order_Item_046(product_id);

CREATE VIEW Cashier_Product_View_046 AS
SELECT
    p.product_id,
    p.product_name,
    c.category_name,
    p.selling_price,
    p.member_discount,
    i.stock_quantity,
    p.status
FROM Products_046 p
JOIN Categories_046 c
    ON p.category_id = c.category_id
JOIN Inventory_046 i
    ON p.product_id = i.product_id
WHERE p.status = 'Available';


SELECT * FROM Cashier_Product_View_046;

CREATE VIEW Management_Product_Sales_View_046 AS
SELECT
    p.product_id,
    p.product_name,
    c.category_name,
    SUM(oi.quantity) AS total_quantity_sold,
    SUM(oi.quantity * oi.unit_price) AS total_sales_amount
FROM Products_046 p
JOIN Categories_046 c
    ON p.category_id = c.category_id
JOIN Order_Item_046 oi
    ON p.product_id = oi.product_id
JOIN Orders_046 o
    ON oi.order_id = o.order_id
WHERE o.status = 'Completed'
GROUP BY
    p.product_id,
    p.product_name,
    c.category_name
ORDER BY total_sales_amount DESC;

SELECT * FROM Management_Product_Sales_View_046;

CREATE VIEW Member_Discount_Product_View_046 AS
SELECT
    p.product_id,
    p.product_name,
    c.category_name,
    p.selling_price,
    p.member_discount,
    i.stock_quantity
FROM Products_046 p
JOIN Categories_046 c
    ON p.category_id = c.category_id
JOIN Inventory_046 i
    ON p.product_id = i.product_id
WHERE p.status = 'Available'
  AND p.member_discount > 0
  AND i.stock_quantity > 0;
  
  SELECT * FROM Member_Discount_Product_View_046;
  
  CREATE TABLE Low_Stock_Warning_046 (
    warning_id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT NOT NULL,
    remaining_stock INT NOT NULL,
    warning_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    message VARCHAR(255),

    CONSTRAINT fk_warning_product
        FOREIGN KEY (product_id)
        REFERENCES Products_046(product_id)
);


DELIMITER $$

CREATE TRIGGER trg_low_stock_warning_046
AFTER INSERT ON Order_Item_046
FOR EACH ROW
BEGIN

    -- Deduct inventory
    UPDATE Inventory_046
    SET stock_quantity = stock_quantity - NEW.quantity
    WHERE product_id = NEW.product_id;

    -- Generate warning if stock falls below reorder level
    INSERT INTO Low_Stock_Warning_046
        (product_id, remaining_stock, message)
    SELECT
        product_id,
        stock_quantity,
        CONCAT('Low stock warning for Product ID ', product_id)
    FROM Inventory_046
    WHERE product_id = NEW.product_id
      AND stock_quantity < reorder_level;

END$$

DELIMITER ;

INSERT INTO Order_Item_046
(quantity, unit_price, order_id, product_id)
VALUES
(45,1200.00,2,1);
SELECT *
FROM Inventory_046
WHERE product_id = 1;


SELECT *
FROM Low_Stock_Warning_046;

DELIMITER $$

CREATE TRIGGER trg_member_points_046
AFTER UPDATE ON Orders_046
FOR EACH ROW
BEGIN

    -- Execute only when order status changes to Completed
    IF NEW.status = 'Completed'
       AND OLD.status <> 'Completed'
       AND NOT EXISTS (
            SELECT 1
            FROM Points_Record_046
            WHERE order_id = NEW.order_id
       )
    THEN

        -- Add points to customer's account
        UPDATE Customers_046
        SET total_points = total_points + FLOOR(NEW.total_amount)
        WHERE customer_id = NEW.customer_id;

        -- Record the earned points
        INSERT INTO Points_Record_046
        (
            points_earned,
            earned_date,
            customer_id,
            order_id
        )
        VALUES
        (
            FLOOR(NEW.total_amount),
            NOW(),
            NEW.customer_id,
            NEW.order_id
        );

    END IF;

END$$

DELIMITER ;

UPDATE Orders_046
SET status = 'Completed'
WHERE order_id = 4;

SELECT
    customer_id,
    name,
    total_points
FROM Customers_046
WHERE customer_id = 4;

SELECT *
FROM Points_Record_046
WHERE order_id = 4;

UPDATE Orders_046
SET status = 'Completed'
WHERE order_id = 4;
  
  INSERT INTO Products_046
(
    product_name,
    description,
    selling_price,
    purchase_price,
    status,
    member_discount,
    category_id,
    supplier_id
)
VALUES
(
    'Wireless Mouse',
    'Bluetooth wireless mouse',
    35.00,
    20.00,
    'Available',
    5.00,
    1,
    1
);

INSERT INTO Inventory_046
(
    stock_quantity,
    reorder_level,
    product_id
)
VALUES
(
    100,
    20,
    LAST_INSERT_ID()
);

INSERT INTO Customers_046
(
    name,
    email,
    phone,
    address,
    membership_level,
    total_points
)
VALUES
(
    'James Anderson',
    'james@gmail.com',
    '6666666666',
    'Boston',
    'Regular',
    0
);

SELECT *
FROM Products_046;
  
  
  SELECT
    product_name,
    selling_price,
    member_discount
FROM Products_046
WHERE status = 'Available';


SELECT *
FROM Orders_046
ORDER BY order_date DESC;

UPDATE Products_046
SET selling_price = 1300.00
WHERE product_id = 1;

UPDATE Customers_046
SET membership_level = 'Gold'
WHERE customer_id = 2;

UPDATE Orders_046
SET status = 'Completed'
WHERE order_id = 2;

DELETE FROM Customers_046
WHERE customer_id = 6;


DELETE FROM Products_046
WHERE product_id = 6;





SELECT * FROM Customers_046;


SELECT * 
FROM Products_046
WHERE status = 'Available';


SELECT * FROM Suppliers_046;

SELECT *
FROM Products_046
WHERE member_discount > 0;

SELECT *
FROM Inventory_046
WHERE stock_quantity < reorder_level;


SELECT *
FROM Orders_046
WHERE status = 'Completed';

SELECT *
FROM Payments_046
WHERE payment_status = 'Paid';


SELECT *
FROM Products_046
ORDER BY selling_price DESC;


SELECT *
FROM Users_046
ORDER BY role;



SELECT
    c.customer_id,
    c.name,
    o.order_id,
    o.order_date,
    o.total_amount,
    o.status
FROM Customers_046 c
JOIN Orders_046 o
ON c.customer_id = o.customer_id;


SELECT
    p.product_name,
    c.category_name,
    s.company_name,
    p.selling_price,
    p.status
FROM Products_046 p
JOIN Categories_046 c
ON p.category_id = c.category_id
JOIN Suppliers_046 s
ON p.supplier_id = s.supplier_id;

SELECT
    o.order_id,
    c.name,
    p.product_name,
    oi.quantity,
    oi.unit_price
FROM Orders_046 o
JOIN Customers_046 c
ON o.customer_id = c.customer_id
JOIN Order_Item_046 oi
ON o.order_id = oi.order_id
JOIN Products_046 p
ON oi.product_id = p.product_id;

SELECT
    c.customer_id,
    c.name,
    SUM(o.total_amount) AS Total_Spent
FROM Customers_046 c
JOIN Orders_046 o
ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.name
ORDER BY Total_Spent DESC;

SELECT
    product_id,
    quantity
FROM Order_Item_046
WHERE quantity >
(
    SELECT AVG(quantity)
    FROM Order_Item_046
);

INSERT INTO Customers_046
(name, email, phone, address, membership_level)
VALUES
('John Smith',
'john@gmail.com',
'1234567890',
'New York',
'Gold');

SELECT *
FROM Customers_046;


UPDATE Customers_046
SET phone = '9876543210',
    membership_level = 'VIP'
WHERE customer_id = 1;
