import asyncio

from telethon import events
from telethon.errors import FloodWaitError
from telethon.tl.types import (
    MessageMediaPhoto,
    MessageMediaDocument,
    MessageMediaWebPage,
)

from core.client import client
from config.env import TARGET_GROUP
from config.forwarding import CHANNEL_TOPIC_MAP, FORWARD_TOPIC_RULES
from utils.logger import setup_logger

logger = setup_logger()

FORWARDED_MAP = {}


def allowed_by_topic_rules(msg, topic_id):
    rules = FORWARD_TOPIC_RULES.get(topic_id)

    if not rules:
        return True

    # ✅ Allow link-only embedded messages (Telegram web previews)
    # Telethon represents these as MessageMediaWebPage with no msg.text
    if (
        msg.text is None
        and isinstance(msg.media, MessageMediaWebPage)
    ):
        return rules.get("text", False)

    if msg.text and not msg.media:
        return rules.get("text", False)

    media = msg.media

    if isinstance(media, MessageMediaPhoto):
        return rules.get("photo", False)

    if msg.video:
        return rules.get("video", False)

    if isinstance(media, MessageMediaDocument):
        allowed = rules.get("doc_ext")
        if allowed is None:
            return True

        filename = msg.file.name or ""
        ext = "." + filename.lower().split(".")[-1] if "." in filename else ""
        return ext in allowed

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


@client.on(events.NewMessage(chats=list(CHANNEL_TOPIC_MAP.keys())))
async def forward_handler(event):
    msg = event.message
    topic_id = CHANNEL_TOPIC_MAP.get(event.chat_id)

    if not msg or not topic_id:
        return

    if not allowed_by_topic_rules(msg, topic_id):
        logger.info(
            "Skipped msg_id=%s due to topic rules (topic=%s)",
            msg.id,
            topic_id
        )
        return

    await safe_forward(msg, topic_id)


@client.on(events.Album(chats=list(CHANNEL_TOPIC_MAP.keys())))
async def album_handler(event):
    topic_id = CHANNEL_TOPIC_MAP.get(event.chat_id)

    if not topic_id:
        return

    for msg in event.messages:
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

    except Exception as e:
        logger.exception("Album forward failed: %s", e)


@client.on(events.MessageEdited(chats=list(CHANNEL_TOPIC_MAP.keys())))
async def edit_handler(event):
    msg = event.message
    topic_id = CHANNEL_TOPIC_MAP.get(event.chat_id)

    if not msg or not topic_id:
        return

    old_fwd = FORWARDED_MAP.pop(msg.id, None)

    try:
        if old_fwd:
            await client.delete_messages(TARGET_GROUP, old_fwd)

        if not allowed_by_topic_rules(msg, topic_id):
            return

        await safe_forward(msg, topic_id)

    except Exception as e:
        logger.exception("Edit handling failed: %s", e)
