import time
from telethon import events

from core.client import client
from core.startup import START_TIME
from utils.stats import get_stats

@client.on(events.NewMessage(pattern="/health"))
async def health_handler(event):
    now = time.time()
    uptime_seconds = int(now - START_TIME)

    hours, remainder = divmod(uptime_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    stats = get_stats()

    text = (
        "🟢 **Bot Health: OK**\n\n"
        f"⏱ Uptime: {hours}h {minutes}m {seconds}s\n\n"
        f"➡️ Forwarded: {stats['forwarded']}\n"
        f"🗑 Deleted: {stats['deleted']}"
    )

    await event.reply(text, parse_mode="md")
