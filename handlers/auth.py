from telethon import events
from core.client import client
from db.database import get_db

@client.on(events.NewMessage(pattern="/login"))
async def login_handler(event):
    sender = await event.get_sender()
    telegram_id = sender.id
    username = sender.username

    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        "SELECT is_active FROM users WHERE telegram_id = ?",
        (telegram_id,)
    )
    row = cur.fetchone()

    if row:
        if row[0]:
            await event.reply("✅ You are already logged in.")
        else:
            await event.reply("⏳ Your access is pending approval.")
    else:
        cur.execute(
            "INSERT INTO users (telegram_id, username) VALUES (?, ?)",
            (telegram_id, username)
        )
        conn.commit()
        await event.reply(
            "📝 Login request submitted.\n"
            "Please wait for admin approval."
        )

    conn.close()
