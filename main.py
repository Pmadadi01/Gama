from fastapi import FastAPI
import sqlite3

app = FastAPI()

# اتصال به دیتابیس
conn = sqlite3.connect("accounting.db")
cursor = conn.cursor()

# ایجاد جدول
cursor.execute("""
CREATE TABLE IF NOT EXISTS entries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    description TEXT,
    debit REAL,
    credit REAL
)
""")
conn.commit()

@app.post("/add-entry/")
async def add_entry(description: str, debit: float, credit: float):
    cursor.execute(
        "INSERT INTO entries (description, debit, credit) VALUES (?, ?, ?)",
        (description, debit, credit)
    )
    conn.commit()
    return {"message": "سند ثبت شد!", "id": cursor.lastrowid}

@app.get("/entries/")
async def get_entries():
    cursor.execute("SELECT * FROM entries")
    return cursor.fetchall()
