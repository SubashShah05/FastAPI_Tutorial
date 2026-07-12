import sqlite3
from fastapi import FastAPI

app = FastAPI()

# Connect to SQLite database
conn = sqlite3.connect("test.db", check_same_thread=False)

# Create cursor
cursor = conn.cursor()

# Create table if it doesn't exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS todos (
    id INTEGER PRIMARY KEY,
    title TEXT,
    completed TEXT
)
""")

# Save changes
conn.commit()

@app.get("/")
def home():
    return {
        "message": "SQLite connected successfully"
    }