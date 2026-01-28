import sqlite3

DB_NAME = "bot.db"


def get_db():
    return sqlite3.connect(DB_NAME)


def init_db():
    db = get_db()
    cur = db.cursor()

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

    db.commit()
    db.close()
