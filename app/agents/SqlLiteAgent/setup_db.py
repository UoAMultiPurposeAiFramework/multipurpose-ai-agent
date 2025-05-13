import sqlite3, os

os.makedirs("db", exist_ok=True)
conn = sqlite3.connect("db/finance_db.sqlite3")
cur = conn.cursor()

cur.executescript("""
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS transactions;

CREATE TABLE users (
    user_id INTEGER PRIMARY KEY,
    name TEXT,
    email TEXT
);

CREATE TABLE transactions (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    amount REAL,
    category TEXT,
    date TEXT
);

INSERT INTO users VALUES (1, 'Alice', 'alice@example.com');
INSERT INTO transactions VALUES 
(1, 1, 23.45, 'Groceries', '2024-05-01'),
(2, 1, 99.99, 'Electronics', '2024-05-02');
""")

conn.commit()
conn.close()
print("DB setup complete.")
