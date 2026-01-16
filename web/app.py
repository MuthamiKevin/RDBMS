from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from rdbms.engine import execute

app = FastAPI(title="Banking RDBMS Demo")

# Initialize DB schema

execute("""
CREATE TABLE customers (
    id INT PRIMARY KEY,
    name TEXT,
    email TEXT UNIQUE
)
""")

execute("""
CREATE TABLE accounts (
    id INT PRIMARY KEY,
    account_number TEXT UNIQUE,
    customer_id INT,
    balance FLOAT
)
""")


# Models
class Customer(BaseModel):
    id: int
    name: str
    email: str

class Account(BaseModel):
    id: int
    account_number: str
    customer_id: int
    balance: float


# Routes
@app.get("/", response_class=HTMLResponse)
def home():
    with open("web/index.html") as f:
        return f.read()

# Customers 
@app.post("/customers")
def create_customer(customer: Customer):
    sql = f"""
    INSERT INTO customers
    VALUES ({customer.id}, '{customer.name}', '{customer.email}')
    """
    return {"result": execute(sql)}

@app.get("/customers")
def get_customers():
    return execute("SELECT * FROM customers")

# Accounts 
@app.post("/accounts")
def create_account(account: Account):
    sql = f"""
    INSERT INTO accounts
    VALUES (
        {account.id},
        '{account.account_number}',
        {account.customer_id},
        {account.balance}
    )
    """
    return {"result": execute(sql)}

@app.get("/accounts")
def get_accounts():
    return execute("SELECT * FROM accounts")

# Banking Operation 
@app.post("/deposit/{account_number}/{amount}")
def deposit(account_number: str, amount: float):
    sql = f"""
    UPDATE accounts
    SET balance = {amount}
    WHERE account_number = '{account_number}'
    """
    return {"result": execute(sql)}
