from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from rdbms.engine import engine

app = FastAPI(title="Simple RDBMS Demo")

# Initialize tables
engine.create_table("customers", ["id", "name", "email"])

# Models
class Customer(BaseModel):
    id: int
    name: str
    email: str


@app.get("/", response_class=HTMLResponse)
def home():
    with open("web/index.html") as f:
        return f.read()


# CREATE
@app.post("/customers")
def create_customer(customer: Customer):
    engine.insert("customers", customer.dict())
    return {"message": "Customer created"}


# READ
@app.get("/customers")
def get_customers():
    return engine.select("customers")


# UPDATE
@app.put("/customers/{customer_id}")
def update_customer(customer_id: int, customer: Customer):
    updated = engine.update(
        "customers",
        ("id", customer_id),
        customer.dict()
    )
    if not updated:
        raise HTTPException(404, "Customer not found")
    return {"message": "Customer updated"}


# DELETE
@app.delete("/customers/{customer_id}")
def delete_customer(customer_id: int):
    deleted = engine.delete("customers", ("id", customer_id))
    if not deleted:
        raise HTTPException(404, "Customer not found")
    return {"message": "Customer deleted"}
