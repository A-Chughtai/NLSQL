import sqlite3

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect("test.db")
cursor = conn.cursor()

# Create USERS table if it doesn't exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS USERS (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    department TEXT NOT NULL
)
""")

# Insert dummy data into USERS table
dummy_users = [
    ("Alice Johnson", "alice@example.com", "Finance"),
    ("Bob Smith", "bob@example.com", "Engineering"),
    ("Carol White", "carol@example.com", "Finance"),
    ("David Brown", "david@example.com", "Marketing"),
    ("Eve Green", "eve@example.com", "Finance")
]

cursor.executemany("""
INSERT INTO USERS (name, email, department)
VALUES (?, ?, ?)
""", dummy_users)

# Commit the changes and close the connection
conn.commit()
print("Database initialized with dummy data.")
cursor.close()
conn.close()
