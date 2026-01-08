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
from utils.forward_map import save_mapping, get_mapping, delete_mapping

logger = setup_logger()

URL_RE = re.compile(r"https?://\S+", re.IGNORECASE)


def _is_raw_link_only(msg):
    if not msg.raw_text:
        return False
    return bool(URL_RE.fullmatch(msg.raw_text.strip()))


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


async def safe_forward(msg, topic_id):
    try:
        fwd = await client.send_message(
            TARGET_GROUP,
            msg,
            reply_to=topic_id
        )

        save_mapping(
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
            save_mapping(
                src.chat_id,
                src.id,
                TARGET_GROUP,
                fwd.id
            )

    except Exception as e:
        logger.exception("Album forward failed: %s", e)


@client.on(events.MessageEdited(chats=list(CHANNEL_TOPIC_MAP.keys())))
async def edit_handler(event):
    msg = event.message
    source_chat_id = event.chat_id

    if not msg:
        return

    mapping = get_mapping(source_chat_id, msg.id)
    if not mapping:
        return

    target_chat_id, target_msg_id = mapping

    try:
        await client.edit_message(
            target_chat_id,
            target_msg_id,
            msg
        )
    except Exception as e:
        logger.exception("Edit sync failed: %s", e)


@client.on(events.MessageDeleted(chats=list(CHANNEL_TOPIC_MAP.keys())))
async def delete_handler(event):
    source_chat_id = event.chat_id

    for msg_id in event.deleted_ids:
        mapping = get_mapping(source_chat_id, msg_id)
        if not mapping:
            continue

        target_chat_id, target_msg_id = mapping

        try:
            await client.delete_messages(
                target_chat_id,
                target_msg_id
            )
            delete_mapping(source_chat_id, msg_id)
        except Exception as e:
            logger.exception("Delete sync failed: %s", e)
