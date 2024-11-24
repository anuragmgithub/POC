CREATE TABLE Customers (
    customer_id INT PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    email VARCHAR(100),
    phone VARCHAR(15),
    address VARCHAR(255)
);

-- Sample Insert Statements
INSERT INTO Customers (customer_id, first_name, last_name, email, phone, address) 
VALUES
(1, 'John', 'Doe', 'john.doe@example.com', '9876543210', '123 Elm Street'),
(2, 'Jane', 'Smith', 'jane.smith@example.com', '9123456789', '456 Oak Avenue');


CREATE TABLE Accounts (
    account_id INT PRIMARY KEY,
    customer_id INT,
    account_type VARCHAR(50),
    balance DECIMAL(15, 2),
    opening_date DATE,
    FOREIGN KEY (customer_id) REFERENCES Customers(customer_id)
);

-- Sample Insert Statements
INSERT INTO Accounts (account_id, customer_id, account_type, balance, opening_date) 
VALUES
(101, 1, 'Savings', 5000.00, '2023-01-15'),
(102, 1, 'Checking', 1500.00, '2023-02-20'),
(103, 2, 'Savings', 8000.00, '2023-03-10');



