import time
from telethon import events

from core.client import client
from core.startup import START_TIME

@client.on(events.NewMessage(pattern="/health"))
async def health_handler(event):
    uptime = int(time.time() - START_TIME)

    hours, remainder = divmod(uptime, 3600)
    minutes, seconds = divmod(remainder, 60)

    await event.reply(
        "🟢 **Bot Health: OK**\n\n"
        f"⏱ Uptime: {hours}h {minutes}m {seconds}s",
        parse_mode="md"
    )
