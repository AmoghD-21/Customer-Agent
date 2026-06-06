# backend/app/tools.py
from langchain_core.tools import tool
from pydantic import BaseModel, Field
import os
import sqlite3

# Dynamically point to the local SQLite database we created in Phase 1
DB_PATH = os.path.join(os.path.dirname(__file__), "../../data/crm.db")

def query_db(query: str, params: tuple = ()):
    """Helper utility to open a safe connection and run SQL against our CRM."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(query, params)
    result = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return result

# --- 1. Customer Profile Schema & Tool ---
class CustomerLookupInput(BaseModel):
    customer_id: str = Field(description="The unique alphanumeric identifier for the customer, e.g., CUST_101")

@tool("get_customer_profile", args_schema=CustomerLookupInput)
def get_customer_profile(customer_id: str) -> str:
    """Fetches the customer's structural profile details, membership status, name, and email from the CRM."""
    query = "SELECT * FROM customers WHERE customer_id = ?"
    results = query_db(query, (customer_id,))
    
    if not results:
        return f"Error: No profile records discovered for Customer ID '{customer_id}'."
    
    customer = results[0]
    return f"Customer Profile Found: Name: {customer['name']}, Email: {customer['email']}, Tier: {customer['tier']}"


# --- 2. Order Tracking Schema & Tool ---
class OrderLookupInput(BaseModel):
    order_id: str = Field(description="The unique alphanumeric order reference identifier, e.g., ORD_1042")

@tool("get_order_status", args_schema=OrderLookupInput)
def get_order_status(order_id: str) -> str:
    """Retrieves real-time fulfillment tracking updates, items purchased, and pricing values from the operations engine."""
    query = "SELECT * FROM orders WHERE order_id = ?"
    results = query_db(query, (order_id,))
    
    if not results:
        return f"Error: Order profile matching ID '{order_id}' was not found in the operations tracking system."
    
    order = results[0]
    return (
        f"Order Details Located:\n"
        f"- Order ID: {order['order_id']}\n"
        f"- Item Name: {order['item_name']}\n"
        f"- Shipping Status: {order['status']}\n"
        f"- Tracking Reference: {order['tracking_number']}\n"
        f"- Total Cost: ${order['price']:.2f}"
    )

# Array list of exposed tools to hand off to our LangChain Agent pipeline later
support_tool_catalog = [get_customer_profile, get_order_status]