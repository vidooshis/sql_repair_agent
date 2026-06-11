import sqlite3

conn = sqlite3.connect("database/company.db")

cursor = conn.cursor()

cursor.execute("SELECT * FROM customers")

rows = cursor.fetchall()

print(rows)

conn.close()