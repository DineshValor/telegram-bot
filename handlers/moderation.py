from telethon import events
from telethon.tl.types import (
    MessageMediaPhoto,
    MessageMediaDocument,
    PeerUser,
)

import asyncio

from core.client import client
from config.env import TARGET_GROUP
from config.moderation import TOPIC_RULES
from utils.messages import send_reason
from utils.logger import setup_logger

logger = setup_logger()


async def is_bot_or_anonymous_admin(msg):
    """
    Returns True if:
    - Message sent by the bot itself
    - Message sent by anonymous admin
    """
    me = await client.get_me()

    # Bot itself
    if msg.from_id and isinstance(msg.from_id, PeerUser):
        if msg.from_id.user_id == me.id:
            return True

    # Anonymous admin
    if msg.from_id is None and msg.post_author:
        return True

    return False


async def auto_delete_later(msg, delay: int):
    """Delete a message after delay (seconds)."""
    try:
        await asyncio.sleep(delay)
        await msg.delete()
    except Exception:
        pass


@client.on(events.NewMessage(chats=TARGET_GROUP))
async def moderation_handler(event):
    msg = event.message

    if not msg or not msg.reply_to:
        return

    # Exempt bot & anonymous admins
    try:
        if await is_bot_or_anonymous_admin(msg):
            return
    except Exception:
        return

    topic_id = msg.reply_to.reply_to_msg_id
    rules = TOPIC_RULES.get(topic_id)

    if not rules:
        return

    # 🔍 DEBUG: Auto-delete rule check
    logger.info(
        "AUTO-DEL CHECK | msg_id=%s topic_id=%s delay=%s reply_to=%s",
        msg.id,
        topic_id,
        rules.get("auto_delete_replies_after"),
        msg.reply_to.reply_to_msg_id if msg.reply_to else None,
    )

    try:
        # =========================
        # ⏳ AUTO DELETE REPLIES
        # =========================
        auto_delete_delay = rules.get("auto_delete_replies_after")

        # Reply inside topic (not the topic root message)
        if (
            auto_delete_delay
            and msg.reply_to
            and msg.id != topic_id
        ):
            logger.info(
                "AUTO-DEL SCHEDULED | msg_id=%s topic_id=%s delete_after=%ss",
                msg.id,
                topic_id,
                auto_delete_delay,
            )

            asyncio.create_task(
                auto_delete_later(msg, auto_delete_delay)
            )

        # =========================
        # 🔁 FORWARDED MESSAGES
        # =========================
        if msg.fwd_from:
            forwarded_allowed = rules.get("forwarded_allowed")

            # ❌ Delete all forwarded messages
            if forwarded_allowed is False:
                await msg.delete()
                logger.warning(
                    "Deleted FORWARDED message | topic=%s | user=%s",
                    topic_id,
                    msg.sender_id
                )
                await send_reason(
                    topic_id,
                    "Forwarded messages are not allowed in this topic.",
                    msg
                )
                return

            # ✅ Allow all forwarded messages
            if forwarded_allowed is True:
                return
            # forwarded_allowed == None → continue to normal rules

        # =========================
        # 📝 TEXT
        # =========================
        if msg.text and not msg.media:
            if not rules.get("text", False):
                await msg.delete()
                logger.warning(
                    "Deleted TEXT | topic=%s | user=%s",
                    topic_id,
                    msg.sender_id
                )
                await send_reason(
                    topic_id,
                    "Text messages are not allowed in this topic.\n\n"
                    "👉 Please use "
                    "[#XFaction-Chat](https://t.me/IngressIN/1)",
                    msg
                )
            return

        media = msg.media

        # =========================
        # 🖼 PHOTO
        # =========================
        if isinstance(media, MessageMediaPhoto):
            if not rules.get("photo", False):
                await msg.delete()
                logger.warning(
                    "Deleted PHOTO | topic=%s | user=%s",
                    topic_id,
                    msg.sender_id
                )
                await send_reason(
                    topic_id,
                    "Photos are not allowed in this topic.",
                    msg
                )
            return

        # =========================
        # 🎥 VIDEO
        # =========================
        if msg.video:
            if not rules.get("video", False):
                await msg.delete()
                logger.warning(
                    "Deleted VIDEO | topic=%s | user=%s",
                    topic_id,
                    msg.sender_id
                )
                await send_reason(
                    topic_id,
                    "Videos are not allowed in this topic.",
                    msg
                )
            return

        # =========================
        # 📦 DOCUMENT
        # =========================
        if isinstance(media, MessageMediaDocument):
            allowed_ext = rules.get("doc_ext")

            # ❌ Block ALL documents
            if allowed_ext is False:
                await msg.delete()
                logger.warning(
                    "Deleted DOCUMENT | topic=%s | user=%s",
                    topic_id,
                    msg.sender_id
                )
                await send_reason(
                    topic_id,
                    "Documents are not allowed in this topic.",
                    msg
                )
                return

            # ✅ Allow all documents
            if allowed_ext is None:
                return

            # ✅ Allow only specific extensions
            filename = msg.file.name or ""
            ext = "." + filename.lower().split(".")[-1] if "." in filename else ""

            if ext not in allowed_ext:
                await msg.delete()
                logger.warning(
                    "Deleted DOC %s | topic=%s | user=%s",
                    ext,
                    topic_id,
                    msg.sender_id
                )
                allowed = ", ".join(sorted(allowed_ext))
                await send_reason(
                    topic_id,
                    f"File type `{ext}` not allowed.\nAllowed: {allowed}",
                    msg
                )
            return

    except Exception as e:
        logger.exception("Moderation error: %s", e)
