import sqlite3
from config import DB_NAME

def get_conn():
    return sqlite3.connect(DB_NAME)

def init_db():
    with get_conn() as conn:
        cur = conn.cursor()

        cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            company TEXT,
            queue TEXT
        )
        """)

        cur.execute("""
        CREATE TABLE IF NOT EXISTS schedules (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company TEXT,
            queue TEXT,
            date TEXT,
            off_time TEXT,
            on_time TEXT
        )
        """)

        conn.commit()
