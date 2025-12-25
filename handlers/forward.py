import asyncio

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
from config.forwarding_topics import FORWARD_TOPIC_RULES
from utils.logger import setup_logger

logger = setup_logger()

# source_msg_id -> forwarded_msg_id
FORWARDED_MAP = {}


# =========================
# Topic rule validation
# =========================

def allowed_by_topic_rules(msg, topic_id):
    rules = FORWARD_TOPIC_RULES.get(topic_id)

    # No rules → allow everything
    if not rules:
        return True

    # 📝 Text
    if msg.text and not msg.media:
        return rules.get("text", False)

    media = msg.media

    # 🖼 Photo
    if isinstance(media, MessageMediaPhoto):
        return rules.get("photo", False)

    # 🎥 Video
    if msg.video:
        return rules.get("video", False)

    # 📦 Document
    if isinstance(media, MessageMediaDocument):
        allowed_ext = rules.get("doc_ext")

        if allowed_ext is None:
            return True

        filename = msg.file.name or ""
        ext = "." + filename.lower().split(".")[-1] if "." in filename else ""
        return ext in allowed_ext

    return False


def allowed_media_channel(msg):
    """Validate media-only channel rules."""
    media = msg.media

    if isinstance(media, MessageMediaPhoto):
        return True

    if isinstance(media, MessageMediaDocument):
        filename = msg.file.name or ""
        ext = "." + filename.lower().split(".")[-1] if "." in filename else ""
        return ext in ALLOWED_EXTENSIONS

    return False


async def safe_forward(msg, topic_id):
    try:
        fwd = await client.send_message(
            TARGET_GROUP,
            msg,
            reply_to=topic_id
        )
        FORWARDED_MAP[msg.id] = fwd.id
        return fwd

    except FloodWaitError as e:
        logger.warning("FloodWait %ss — sleeping", e.seconds)
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

    if not msg or not topic_id:
        return

    # Media-only channel enforcement
    if chat_id in MEDIA_ONLY_CHANNELS:
        if not msg.media or not allowed_media_channel(msg):
            return

    # Topic-based rules
    if not allowed_by_topic_rules(msg, topic_id):
        logger.info(
            "Skipped msg_id=%s (topic rules) → topic=%s",
            msg.id,
            topic_id
        )
        return

    await safe_forward(msg, topic_id)


# =========================
# Album handler
# =========================

@client.on(events.Album(chats=list(CHANNEL_TOPIC_MAP.keys())))
async def album_handler(event):
    chat_id = event.chat_id
    topic_id = CHANNEL_TOPIC_MAP.get(chat_id)

    if not topic_id:
        return

    for msg in event.messages:
        # Media-only channel rules
        if chat_id in MEDIA_ONLY_CHANNELS and not allowed_media_channel(msg):
            return

        # Topic rules
        if not allowed_by_topic_rules(msg, topic_id):
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
            "Forwarded album (%s msgs) → topic=%s",
            len(event.messages),
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

    if not msg or not topic_id:
        return

    old_fwd_id = FORWARDED_MAP.pop(msg.id, None)

    try:
        if old_fwd_id:
            await client.delete_messages(TARGET_GROUP, old_fwd_id)

        # Re-check rules
        if chat_id in MEDIA_ONLY_CHANNELS:
            if not msg.media or not allowed_media_channel(msg):
                return

        if not allowed_by_topic_rules(msg, topic_id):
            return

        await safe_forward(msg, topic_id)

    except Exception as e:
        logger.exception("Edit repost failed: %s", e)
