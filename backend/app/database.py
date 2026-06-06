# backend/app/database.py
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "../../data/crm.db")

def get_db_connection():
    """Establishes and returns a connection to the SQLite database."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Allows us to access columns by name like a dictionary
    return conn

def init_db():
    """Initializes the database tables and inserts mock data."""
    # Ensure data directory exists
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    
    conn = get_db_connection()
    cursor = conn.cursor()

    # 1. Create Customers Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS customers (
            customer_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            tier TEXT DEFAULT 'Standard'
        )
    ''')

    # 2. Create Orders Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            order_id TEXT PRIMARY KEY,
            customer_id TEXT,
            item_name TEXT NOT NULL,
            status TEXT NOT NULL,
            tracking_number TEXT,
            price REAL,
            FOREIGN KEY (customer_id) REFERENCES customers (customer_id)
        )
    ''')

    # 3. Insert Mock Data (Clear old data first to avoid duplicates during testing)
    cursor.execute("DELETE FROM customers")
    cursor.execute("DELETE FROM orders")

    mock_customers = [
        ("CUST_101", "Alex Rivera", "alex.rivera@email.com", "Premium"),
        ("CUST_102", "Sam Chen", "sam.chen@email.com", "Standard")
    ]

    mock_orders = [
        ("ORD_1042", "CUST_101", "Wireless Noise-Canceling Headphones", "Delayed at local facility", "UPS-77294", 149.99),
        ("ORD_1043", "CUST_102", "Ergonomic Office Chair", "Delivered", "DHL-44129", 249.50)
    ]

    cursor.executemany("INSERT INTO customers VALUES (?, ?, ?, ?)", mock_customers)
    cursor.executemany("INSERT INTO orders VALUES (?, ?, ?, ?, ?, ?)", mock_orders)

    conn.commit()
    conn.close()
    print(f"Database successfully initialized and saved at: {DB_PATH}")

if __name__ == "__main__":
    init_db()