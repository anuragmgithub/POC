from faker import Faker
from sqlalchemy import create_engine, Column, Integer, String, DECIMAL, Date, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from random import randint, choice
from dotenv import load_dotenv
import os

# Initialize Faker and SQLAlchemy
fake = Faker()
load_dotenv()

# Load database connection details
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_DB = os.getenv("MYSQL_DB")
connection_string = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DB}"
engine = create_engine(connection_string, echo=True)

# SQLAlchemy setup
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

# Define tables
class Customer(Base):
    __tablename__ = 'customers'
    customer_id = Column(Integer, primary_key=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    email = Column(String(100))
    phone = Column(String(30))
    address = Column(String(255))
    accounts = relationship("Account", back_populates="customer")

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

# Create tables
Base.metadata.create_all(engine)

# Data generation
def generate_fake_data():
    # Customers
    customers_data = [
        {
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
            'email': fake.email(),
            'phone': fake.phone_number(),
            'address': fake.address()
        } for _ in range(10)
    ]
    session.bulk_insert_mappings(Customer, customers_data)
    session.commit()

    # Accounts
    accounts_data = [
        {
            'customer_id': customer.customer_id,
            'account_type': choice(['Savings', 'Checking']),
            'balance': round(randint(1000, 10000) + randint(0, 99), 2),
            'opening_date': fake.date_this_decade()
        } for customer in session.query(Customer).all()
    ]
    session.bulk_insert_mappings(Account, accounts_data)
    session.commit()

    # Transactions
    transactions_data = [
        {
            'account_id': account.account_id,
            'transaction_type': choice(['Deposit', 'Withdrawal']),
            'amount': round(randint(100, 5000) + randint(0, 99), 2),
            'transaction_date': fake.date_this_year()
        }
        for account in session.query(Account).all()
        for _ in range(5)
    ]
    session.bulk_insert_mappings(Transaction, transactions_data)
    session.commit()

generate_fake_data()
session.close()
