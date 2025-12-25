from telethon import events
from telethon.errors import FloodWaitError
from telethon.tl.types import MessageMediaPhoto, MessageMediaDocument

from core.client import client
from config.env import TARGET_GROUP
from config.forwarding import (
    CHANNEL_TOPIC_MAP,
    MEDIA_ONLY_CHANNELS,
    ALLOWED_EXTENSIONS,
)
from utils.logger import setup_logger

import asyncio

logger = setup_logger()

# source_msg_id -> forwarded_msg_id
FORWARDED_MAP = {}


# =========================
# Utility helpers
# =========================

def is_allowed_media(msg):
    """Validate media based on configured rules."""
    media = msg.media

    if isinstance(media, MessageMediaPhoto):
        return True

    if isinstance(media, MessageMediaDocument):
        filename = msg.file.name or ""
        ext = "." + filename.lower().split(".")[-1] if "." in filename else ""
        return ext in ALLOWED_EXTENSIONS

    return False


async def safe_forward(msg, topic_id):
    """Forward message safely and track mapping."""
    try:
        fwd = await client.send_message(
            TARGET_GROUP,
            msg,
            reply_to=topic_id
        )
        FORWARDED_MAP[msg.id] = fwd.id
        return fwd

    except FloodWaitError as e:
        logger.warning("Flood wait %ss — sleeping", e.seconds)
        await asyncio.sleep(e.seconds)
        return await safe_forward(msg, topic_id)

    except Exception as e:
        logger.exception("Forward failed: %s", e)
        return None


# =========================
# New message handler
# =========================

@client.on(events.NewMessage(chats=list(CHANNEL_TOPIC_MAP.keys())))
async def forward_handler(event):
    msg = event.message
    chat_id = event.chat_id
    topic_id = CHANNEL_TOPIC_MAP.get(chat_id)

    if not topic_id or not msg:
        return

    # Media-only channel logic
    if chat_id in MEDIA_ONLY_CHANNELS:
        if not msg.media or not is_allowed_media(msg):
            return

    await safe_forward(msg, topic_id)

    logger.info(
        "Forwarded msg_id=%s from chat_id=%s → topic_id=%s",
        msg.id,
        chat_id,
        topic_id
    )


# =========================
# Album handler
# =========================

@client.on(events.Album(chats=list(CHANNEL_TOPIC_MAP.keys())))
async def album_handler(event):
    chat_id = event.chat_id
    topic_id = CHANNEL_TOPIC_MAP.get(chat_id)

    if not topic_id:
        return

    # Media-only channel → allow albums only if all media valid
    if chat_id in MEDIA_ONLY_CHANNELS:
        for msg in event.messages:
            if not is_allowed_media(msg):
                return

    try:
        fwd_msgs = await client.send_message(
            TARGET_GROUP,
            event.messages,
            reply_to=topic_id
        )

        for src, fwd in zip(event.messages, fwd_msgs):
            FORWARDED_MAP[src.id] = fwd.id

        logger.info(
            "Forwarded album (%s msgs) from chat_id=%s → topic_id=%s",
            len(event.messages),
            chat_id,
            topic_id
        )

    except Exception as e:
        logger.exception("Album forward failed: %s", e)


# =========================
# Edit handler (delete & repost)
# =========================

@client.on(events.MessageEdited(chats=list(CHANNEL_TOPIC_MAP.keys())))
async def edit_handler(event):
    msg = event.message
    chat_id = event.chat_id
    topic_id = CHANNEL_TOPIC_MAP.get(chat_id)

    if not topic_id or not msg:
        return

    old_fwd_id = FORWARDED_MAP.pop(msg.id, None)

    try:
        if old_fwd_id:
            await client.delete_messages(TARGET_GROUP, old_fwd_id)

        # Re-apply media rules
        if chat_id in MEDIA_ONLY_CHANNELS:
            if not msg.media or not is_allowed_media(msg):
                return

        await safe_forward(msg, topic_id)

        logger.info(
            "Reposted edited msg_id=%s from chat_id=%s",
            msg.id,
            chat_id
        )

    except Exception as e:
        logger.exception("Edit handling failed: %s", e)
