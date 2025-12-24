import sqlite3

DB_FILE = "bot.db"

def get_db():
    return sqlite3.connect(DB_FILE)

def init_db():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            telegram_id INTEGER PRIMARY KEY,
            username TEXT,
            is_admin INTEGER DEFAULT 0,
            is_active INTEGER DEFAULT 0
        )
    """)

    conn.commit()
    conn.close()
