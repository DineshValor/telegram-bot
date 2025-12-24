from db.database import get_db

def is_authorized(telegram_id: int) -> bool:
    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        "SELECT is_active FROM users WHERE telegram_id = ?",
        (telegram_id,)
    )

    row = cur.fetchone()
    conn.close()

    return bool(row and row[0])
