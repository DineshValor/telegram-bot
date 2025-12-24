from telethon import events
from core.client import client
from utils.stats import get_stats

@client.on(events.NewMessage(pattern="/stats"))
async def stats_handler(event):
    stats = get_stats()

    text = (
        "📊 **Bot Statistics**\n\n"
        f"➡️ Forwarded messages: {stats['forwarded']}\n"
        f"🗑 Deleted messages: {stats['deleted']}\n\n"
        "📌 Per-topic:\n"
    )

    for topic, count in stats["per_topic"].items():
        text += f"- Topic `{topic}`: {count}\n"

    await event.reply(text, parse_mode="md")
