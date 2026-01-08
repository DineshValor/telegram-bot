import sqlite3
from pathlib import Path

DB_PATH = Path("delete_map.db")

conn = sqlite3.connect(DB_PATH)
conn.execute("""
CREATE TABLE IF NOT EXISTS delete_map (
    source_chat_id INTEGER,
    source_msg_id  INTEGER,
    target_chat_id INTEGER,
    target_msg_id  INTEGER,
    PRIMARY KEY (source_chat_id, source_msg_id)
)
""")
conn.commit()


def save_map(sc, sm, tc, tm):
    conn.execute(
        "INSERT OR REPLACE INTO delete_map VALUES (?, ?, ?, ?)",
        (sc, sm, tc, tm)
    )
    conn.commit()


def get_map(sc, sm):
    cur = conn.execute(
        "SELECT target_chat_id, target_msg_id FROM delete_map "
        "WHERE source_chat_id=? AND source_msg_id=?",
        (sc, sm)
    )
    return cur.fetchone()


def delete_map_entry(sc, sm):
    conn.execute(
        "DELETE FROM delete_map WHERE source_chat_id=? AND source_msg_id=?",
        (sc, sm)
    )
    conn.commit()
