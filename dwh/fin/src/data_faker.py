from faker import Faker
from sqlalchemy import create_engine, Column, Integer, String, DECIMAL, Date, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from random import randint, choice
import pandas as pd
from dotenv import load_dotenv
import os

# Initialize Faker and SQLAlchemy
fake = Faker()

# Load the .env file
load_dotenv()

# Now you can access the variables
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_DB = os.getenv("MYSQL_DB")

# Build the connection string
connection_string = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DB}"


# Create the engine object using SQLAlchemy's create_engine
engine = create_engine(connection_string, echo=True)


Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

# ORM-mapped classes

class Customer(Base):
    __tablename__ = 'customers'
    customer_id = Column(Integer, primary_key=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    email = Column(String(100))
    phone = Column(String(30))
    address = Column(String(255))

    accounts = relationship("Account", back_populates="customer")
    loans = relationship("Loan", back_populates="customer")
    credit_cards = relationship("CreditCard", back_populates="customer")

class Account(Base):
    __tablename__ = 'accounts'
    account_id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey('customers.customer_id'))
    account_type = Column(String(50))
    balance = Column(DECIMAL(15, 2))
    opening_date = Column(Date)

    customer = relationship("Customer", back_populates="accounts")
    transactions = relationship("Transaction", back_populates="account")

class Transaction(Base):
    __tablename__ = 'transactions'
    transaction_id = Column(Integer, primary_key=True)
    account_id = Column(Integer, ForeignKey('accounts.account_id'))
    transaction_type = Column(String(50))
    amount = Column(DECIMAL(15, 2))
    transaction_date = Column(Date)

    account = relationship("Account", back_populates="transactions")

class Loan(Base):
    __tablename__ = 'loans'
    loan_id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey('customers.customer_id'))
    loan_amount = Column(DECIMAL(15, 2))
    loan_date = Column(Date)
    interest_rate = Column(DECIMAL(5, 2))
    loan_term = Column(Integer)  # months

    customer = relationship("Customer", back_populates="loans")

class CreditCard(Base):
    __tablename__ = 'credit_cards'
    card_id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey('customers.customer_id'))
    card_type = Column(String(50))
    credit_limit = Column(DECIMAL(15, 2))
    balance_due = Column(DECIMAL(15, 2))

    customer = relationship("Customer", back_populates="credit_cards")

class Branch(Base):
    __tablename__ = 'branches'
    branch_id = Column(Integer, primary_key=True)
    branch_name = Column(String(100))
    location = Column(String(255))

    employees = relationship("Employee", back_populates="branch")

class Employee(Base):
    __tablename__ = 'employees'
    employee_id = Column(Integer, primary_key=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    branch_id = Column(Integer, ForeignKey('branches.branch_id'))
    position = Column(String(50))

    branch = relationship("Branch", back_populates="employees")
    audit_logs = relationship("AuditLog", back_populates="employee")

class AuditLog(Base):
    __tablename__ = 'audit_logs'
    log_id = Column(Integer, primary_key=True)
    action = Column(String(50))
    timestamp = Column(Date)
    employee_id = Column(Integer, ForeignKey('employees.employee_id'))

    employee = relationship("Employee", back_populates="audit_logs")

# Create all Tables in the database
Base.metadata.create_all(engine)

# Function to Generate Fake Data
def generate_fake_data():
    # Generate Fake Customers
    customers_data = []
    for _ in range(10):  # 10 customers as an example
        customers_data.append({
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
            'email': fake.email(),
            'phone': fake.phone_number()[:15],
            'address': fake.address()
        })
    
    # Insert Customers
    session.bulk_insert_mappings(Customer, customers_data)
    session.commit()

    # Generate Fake Branches
    branches_data = []
    for _ in range(3):  # 3 branches
        branches_data.append({
            'branch_name': fake.company(),
            'location': fake.address()
        })
    
    # Insert Branches
    session.bulk_insert_mappings(Branch, branches_data)
    session.commit()

    # Generate Fake Employees
    employees_data = []
    branch_ids = [branch.branch_id for branch in session.query(Branch).all()]
    for _ in range(5):  # 5 employees
        employees_data.append({
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
            'branch_id': choice(branch_ids),
            'position': choice(['Manager', 'Clerk', 'Teller'])
        })
    
    # Insert Employees
    session.bulk_insert_mappings(Employee, employees_data)
    session.commit()

    # Generate Fake Accounts
    accounts_data = []
    for customer in session.query(Customer).all():
        account_type = choice(['Savings', 'Checking', 'Business'])
        balance = round(randint(1000, 10000) + randint(0, 99), 2)
        opening_date = fake.date_this_decade()
        accounts_data.append({
            'customer_id': customer.customer_id,
            'account_type': account_type,
            'balance': balance,
            'opening_date': opening_date
        })
    
    # Insert Accounts
    session.bulk_insert_mappings(Account, accounts_data)
    session.commit()

    # Generate Fake Transactions
    transactions_data = []
    for account in session.query(Account).all():
        for _ in range(5):  # 5 transactions per account
            transaction_type = choice(['Deposit', 'Withdrawal'])
            amount = round(randint(100, 5000) + randint(0, 99), 2)
            transaction_date = fake.date_this_decade()
            transactions_data.append({
                'account_id': account.account_id,
                'transaction_type': transaction_type,
                'amount': amount,
                'transaction_date': transaction_date
            })
    
    # Insert Transactions
    session.bulk_insert_mappings(Transaction, transactions_data)
    session.commit()

    # Generate Fake Loans
    loans_data = []
    for customer in session.query(Customer).all():
        loan_amount = round(randint(1000, 50000) + randint(0, 99), 2)
        loan_date = fake.date_this_decade()
        interest_rate = round(randint(3, 10) + randint(0, 99)/100, 2)
        loan_term = choice([12, 24, 36])  # months
        loans_data.append({
            'customer_id': customer.customer_id,
            'loan_amount': loan_amount,
            'loan_date': loan_date,
            'interest_rate': interest_rate,
            'loan_term': loan_term
        })
    
    # Insert Loans
    session.bulk_insert_mappings(Loan, loans_data)
    session.commit()

    # Generate Fake Credit Cards
    credit_cards_data = []
    for customer in session.query(Customer).all():
        credit_limit = round(randint(5000, 50000) + randint(0, 99), 2)
        balance_due = round(randint(0, credit_limit) + randint(0, 99), 2)
        credit_cards_data.append({
            'customer_id': customer.customer_id,
            'card_type': choice(['Visa', 'MasterCard', 'American Express']),
            'credit_limit': credit_limit,
            'balance_due': balance_due
        })
    
    # Insert Credit Cards
    session.bulk_insert_mappings(CreditCard, credit_cards_data)
    session.commit()

    # Generate Fake Audit Logs
    audit_logs_data = []
    employee_ids = [emp.employee_id for emp in session.query(Employee).all()]
    for _ in range(5):  # 5 audit logs
        action = choice(['Account Created', 'Loan Disbursed', 'Transaction Processed'])
        timestamp = fake.date_this_decade()
        employee_id = choice(employee_ids)
        audit_logs_data.append({
            'action': action,
            'timestamp': timestamp,
            'employee_id': employee_id
        })
    
    # Insert Audit Logs
    session.bulk_insert_mappings(AuditLog, audit_logs_data)
    session.commit()

# Generate and Insert Data
generate_fake_data()

# Close
