CREATE TABLE Customers (
    customer_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(15),
    city VARCHAR(50),
    country VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO Customers (customer_name, email, phone, city, country) VALUES
('John Doe', 'john.doe@example.com', '1234567890', 'New York', 'USA'),
('Jane Smith', 'jane.smith@example.com', '9876543210', 'London', 'UK'),
('Rajesh Kumar', 'rajesh.kumar@example.com', '5566778899', 'Delhi', 'India'),
('Maria Gonzalez', 'maria.gonzalez@example.com', '6677889900', 'Madrid', 'Spain'),
('Ahmed Ali', 'ahmed.ali@example.com', '7788990011', 'Cairo', 'Egypt');

CREATE TABLE Categories (
    category_id INT AUTO_INCREMENT PRIMARY KEY,
    category_name VARCHAR(50) NOT NULL,
    description TEXT
);

INSERT INTO Categories (category_name, description) VALUES
('Electronics', 'Devices and gadgets'),
('Clothing', 'Apparel and accessories'),
('Home & Kitchen', 'Home appliances and kitchenware'),
('Books', 'Books and stationery'),
('Sports', 'Sports equipment and gear');


CREATE TABLE Products (
    product_id INT AUTO_INCREMENT PRIMARY KEY,
    product_name VARCHAR(100) NOT NULL,
    category_id INT,
    price DECIMAL(10, 2) NOT NULL,
    stock INT DEFAULT 0,
    FOREIGN KEY (category_id) REFERENCES Categories(category_id)
);

INSERT INTO Products (product_name, category_id, price, stock) VALUES
('Smartphone', 1, 699.99, 100),
('Laptop', 1, 1099.99, 50),
('T-shirt', 2, 19.99, 200),
('Cookware Set', 3, 89.99, 150),
('Yoga Mat', 5, 29.99, 120);


CREATE TABLE Orders (
    order_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT,
    order_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    total_amount DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES Customers(customer_id)
);

INSERT INTO Orders (customer_id, order_date, total_amount) VALUES
(1, '2024-10-01 14:32:00', 749.99),
(2, '2024-10-02 09:15:00', 39.99),
(3, '2024-10-03 17:45:00', 129.99),
(4, '2024-10-04 11:25:00', 299.99),
(5, '2024-10-05 13:50:00', 109.99);


CREATE TABLE OrderItems (
    order_item_id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT,
    product_id INT,
    quantity INT NOT NULL,
    subtotal DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (order_id) REFERENCES Orders(order_id),
    FOREIGN KEY (product_id) REFERENCES Products(product_id)
);

INSERT INTO OrderItems (order_id, product_id, quantity, subtotal) VALUES
(1, 1, 1, 699.99),
(2, 3, 2, 39.98),
(3, 4, 1, 89.99),
(4, 5, 1, 29.99),
(4, 1, 1, 269.99),
(5, 2, 1, 109.99);


CREATE TABLE Inventory (
    inventory_id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT,
    stock INT NOT NULL,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES Products(product_id)
);

INSERT INTO Inventory (product_id, stock) VALUES
(1, 95),
(2, 49),
(3, 198),
(4, 149),
(5, 119);


CREATE TABLE Payments (
    payment_id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT,
    payment_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    payment_method ENUM('Credit Card', 'Debit Card', 'Net Banking', 'Cash on Delivery', 'Wallet'),
    amount DECIMAL(10, 2) NOT NULL,
    status ENUM('Success', 'Pending', 'Failed'),
    FOREIGN KEY (order_id) REFERENCES Orders(order_id)
);

INSERT INTO Payments (order_id, payment_date, payment_method, amount, status) VALUES
(1, '2024-10-01 14:35:00', 'Credit Card', 749.99, 'Success'),
(2, '2024-10-02 09:20:00', 'Wallet', 39.99, 'Success'),
(3, '2024-10-03 17:50:00', 'Net Banking', 129.99, 'Pending'),
(4, '2024-10-04 11:30:00', 'Credit Card', 299.99, 'Success'),
(5, '2024-10-05 13:55:00', 'Cash on Delivery', 109.99, 'Pending');


CREATE TABLE Shipping (
    shipment_id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT,
    shipping_address TEXT,
    city VARCHAR(50),
    country VARCHAR(50),
    postal_code VARCHAR(10),
    shipping_status ENUM('Pending', 'Shipped', 'Delivered', 'Cancelled'),
    shipped_date DATETIME,
    delivery_date DATETIME,
    FOREIGN KEY (order_id) REFERENCES Orders(order_id)
);

INSERT INTO Shipping (order_id, shipping_address, city, country, postal_code, shipping_status, shipped_date, delivery_date) VALUES
(1, '123 Main St', 'New York', 'USA', '10001', 'Delivered', '2024-10-02 08:00:00', '2024-10-03 12:00:00'),
(2, '456 High St', 'London', 'UK', 'WC2N', 'Delivered', '2024-10-03 09:00:00', '2024-10-04 14:00:00'),
(3, '789 Market St', 'Delhi', 'India', '110001', 'Shipped', '2024-10-04 11:00:00', NULL),
(4, '321 Elm St', 'Madrid', 'Spain', '28001', 'Shipped', '2024-10-05 10:00:00', NULL),
(5, '654 Pine St', 'Cairo', 'Egypt', '11511', 'Pending', NULL, NULL);


CREATE TABLE Reviews (
    review_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT,
    product_id INT,
    rating INT CHECK (rating BETWEEN 1 AND 5),
    review_text TEXT,
    review_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES Customers(customer_id),
    FOREIGN KEY (product_id) REFERENCES Products(product_id)
);

INSERT INTO Reviews (customer_id, product_id, rating, review_text) VALUES
(1, 1, 5, 'Amazing smartphone!'),
(2, 3, 4, 'Good quality T-shirt.'),
(3, 4, 3, 'Decent cookware set.'),
(4, 5, 5, 'Best yoga mat I have ever used!'),
(5, 2, 4, 'The laptop is quite good for the price.');


CREATE TABLE Campaigns (
    campaign_id INT AUTO_INCREMENT PRIMARY KEY,
    campaign_name VARCHAR(100),
    start_date DATE,
    end_date DATE,
    budget DECIMAL(10, 2),
    revenue_generated DECIMAL(10, 2)
);

INSERT INTO Campaigns (campaign_name, start_date, end_date, budget, revenue_generated) VALUES
('Holiday Sale', '2024-12-01', '2024-12-31', 50000.00, 150000.00),
('Summer Deals', '2024-06-01', '2024-06-30', 30000.00, 80000.00),
('Black Friday', '2024-11-28', '2024-11-30', 70000.00, 200000.00),
('New Year Offer', '2024-01-01', '2024-01-10', 20000.00, 50000.00);


CREATE TABLE CampaignAnalytics (
    campaign_analytics_id INT AUTO_INCREMENT PRIMARY KEY,
    campaign_id INT,
    customer_id INT,
    engagement_type ENUM('Email Click', 'Purchase', 'Website Visit'),
    engagement_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (campaign_id) REFERENCES Campaigns(campaign_id),
    FOREIGN KEY (customer_id) REFERENCES Customers(customer_id)
);

INSERT INTO CampaignAnalytics (campaign_id, customer_id, engagement_type) VALUES
(1, 1, 'Purchase'),
(1, 2, 'Email Click'),
(2, 3, 'Website Visit'),
(3, 4, 'Purchase'),
(4, 5, 'Email Click');





