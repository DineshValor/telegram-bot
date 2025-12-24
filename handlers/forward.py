from telethon import events
from telethon.tl.types import MessageMediaPhoto, MessageMediaDocument

from core.client import client
from config.env import TARGET_GROUP
from config.forwarding import (
    CHANNEL_TOPIC_MAP,
    MEDIA_ONLY_CHANNELS,
    ALLOWED_EXTENSIONS,
)

@client.on(events.NewMessage)
async def forward_handler(event):
    chat_id = event.chat_id

    if chat_id not in CHANNEL_TOPIC_MAP:
        return

    topic_id = CHANNEL_TOPIC_MAP[chat_id]
    msg = event.message
    media = msg.media

    if chat_id in MEDIA_ONLY_CHANNELS:
        if not media:
            return

        if isinstance(media, MessageMediaPhoto):
            return

        if isinstance(media, MessageMediaDocument):
            filename = msg.file.name or ""
            ext = "." + filename.lower().split(".")[-1] if "." in filename else ""
            if ext not in ALLOWED_EXTENSIONS:
                return
        else:
            return

    await client.send_message(
        TARGET_GROUP,
        msg,
        reply_to=topic_id
    )

    print(f"✅ Forwarded from {chat_id}")
