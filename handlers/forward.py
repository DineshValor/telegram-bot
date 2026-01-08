import asyncio
import re

from telethon import events
from telethon.errors import FloodWaitError
from telethon.tl.types import (
    MessageMediaPhoto,
    MessageMediaDocument,
    MessageMediaWebPage,
    MessageEntityUrl,
    MessageEntityTextUrl,
)

from core.client import client
from config.env import TARGET_GROUP
from config.forwarding import CHANNEL_TOPIC_MAP, FORWARD_TOPIC_RULES
from utils.logger import setup_logger
from utils.delete_map import save_map, get_map, delete_map_entry

logger = setup_logger()

URL_RE = re.compile(r"https?://\S+", re.IGNORECASE)


# -----------------------------
# Helper: raw URL-only messages
# -----------------------------
def _is_raw_link_only(msg):
    if not msg.raw_text:
        return False
    return bool(URL_RE.fullmatch(msg.raw_text.strip()))


# -----------------------------
# Topic-based rule evaluation
# -----------------------------
def allowed_by_topic_rules(msg, topic_id):
    rules = FORWARD_TOPIC_RULES.get(topic_id)

    if not rules:
        return True

    # Case 1: Telegram web preview
    if isinstance(msg.media, MessageMediaWebPage):
        return rules.get("link", rules.get("text", False))

    # Case 2: URL entities only
    if msg.entities:
        for ent in msg.entities:
            if not isinstance(ent, (MessageEntityUrl, MessageEntityTextUrl)):
                break
        else:
            return rules.get("link", rules.get("text", False))

    # Case 3: Raw URL only (no preview, no entities)
    if not msg.media and not msg.text and _is_raw_link_only(msg):
        return rules.get("link", rules.get("text", False))

    # Plain text (including text + link)
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


# -----------------------------
# Safe forward (stock behavior)
# -----------------------------
async def safe_forward(msg, topic_id):
    try:
        fwd = await client.send_message(
            TARGET_GROUP,
            msg,
            reply_to=topic_id
        )

        # Save mapping for delete-sync
        save_map(
            msg.chat_id,
            msg.id,
            TARGET_GROUP,
            fwd.id
        )

        return fwd

    except FloodWaitError as e:
        logger.warning("FloodWait %ss — sleeping", e.seconds)
        await asyncio.sleep(e.seconds)
        return await safe_forward(msg, topic_id)

    except Exception as e:
        logger.exception("Forward failed: %s", e)
        return None


# -----------------------------
# New message forwarding
# -----------------------------
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


# -----------------------------
# Album forwarding (stock)
# -----------------------------
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
            save_map(
                src.chat_id,
                src.id,
                TARGET_GROUP,
                fwd.id
            )

    except Exception as e:
        logger.exception("Album forward failed: %s", e)


# -----------------------------
# Edit handler (STOCK behavior)
# -----------------------------
@client.on(events.MessageEdited(chats=list(CHANNEL_TOPIC_MAP.keys())))
async def edit_handler(event):
    msg = event.message
    topic_id = CHANNEL_TOPIC_MAP.get(event.chat_id)

    if not msg or not topic_id:
        return

    try:
        if not allowed_by_topic_rules(msg, topic_id):
            return

        await safe_forward(msg, topic_id)

    except Exception as e:
        logger.exception("Edit handling failed: %s", e)


# -----------------------------
# DELETE SYNC (NEW, SAFE)
# -----------------------------
@client.on(events.MessageDeleted(chats=list(CHANNEL_TOPIC_MAP.keys())))
async def delete_sync_handler(event):
    source_chat_id = event.chat_id

    for msg_id in event.deleted_ids:
        mapping = get_map(source_chat_id, msg_id)
        if not mapping:
            continue

        target_chat_id, target_msg_id = mapping

        try:
            await client.delete_messages(
                target_chat_id,
                target_msg_id
            )
            delete_map_entry(source_chat_id, msg_id)

            logger.info(
                "Delete sync: source %s:%s → target %s:%s",
                source_chat_id,
                msg_id,
                target_chat_id,
                target_msg_id
            )

        except Exception as e:
            logger.exception("Delete sync failed: %s", e)
