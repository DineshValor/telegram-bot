import sqlite3
from pathlib import Path

DB_PATH = Path("forward_map.db")

conn = sqlite3.connect(DB_PATH)
conn.execute("""
CREATE TABLE IF NOT EXISTS forwarded_messages (
    source_chat_id INTEGER,
    source_msg_id  INTEGER,
    target_chat_id INTEGER,
    target_msg_id  INTEGER,
    PRIMARY KEY (source_chat_id, source_msg_id)
)
""")
conn.commit()


def save_mapping(source_chat_id, source_msg_id, target_chat_id, target_msg_id):
    conn.execute(
        "INSERT OR REPLACE INTO forwarded_messages VALUES (?, ?, ?, ?)",
        (source_chat_id, source_msg_id, target_chat_id, target_msg_id)
    )
    conn.commit()


def get_mapping(source_chat_id, source_msg_id):
    cur = conn.execute(
        "SELECT target_chat_id, target_msg_id FROM forwarded_messages "
        "WHERE source_chat_id=? AND source_msg_id=?",
        (source_chat_id, source_msg_id)
    )
    return cur.fetchone()


def delete_mapping(source_chat_id, source_msg_id):
    conn.execute(
        "DELETE FROM forwarded_messages WHERE source_chat_id=? AND source_msg_id=?",
        (source_chat_id, source_msg_id)
    )
    conn.commit()
