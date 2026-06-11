import sqlite3

conn = sqlite3.connect("database/company.db")

cursor = conn.cursor()

cursor.execute("""
DROP TABLE IF EXISTS customers
""")

cursor.execute("""
CREATE TABLE customers (
    id INTEGER PRIMARY KEY,
    customer_name TEXT,
    customer_email TEXT,
    age INTEGER
)
""")

cursor.executemany(
    """
    INSERT INTO customers
    VALUES (?, ?, ?, ?)
    """,
    [
        (1, "Alice", "alice@test.com", 25),
        (2, "Bob", "bob@test.com", 30),
        (3, "Charlie", "charlie@test.com", 35),
    ]
)

conn.commit()
conn.close()

print("Database created successfully")