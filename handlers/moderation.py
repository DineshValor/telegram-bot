from telethon import events
from telethon.tl.types import (
    MessageMediaPhoto,
    MessageMediaDocument,
    PeerUser,
)

from core.client import client
from config.env import TARGET_GROUP
from config.moderation import TOPIC_RULES
from utils.messages import send_reason
from utils.logger import setup_logger

logger = setup_logger()


async def is_bot_or_anonymous_admin(msg):
    me = await client.get_me()

    # Bot itself
    if msg.from_id and isinstance(msg.from_id, PeerUser):
        return msg.from_id.user_id == me.id

    # Anonymous admin
    if msg.from_id is None and msg.post_author:
        return True

    return False


def resolve_topic_id(event, msg):
    """
    Resolve forum topic ID safely for:
    - direct topic messages
    - replies
    - nested replies
    Works on old & new Telethon
    """

    # 1️⃣ Replies (most reliable)
    if msg.reply_to:
        return (
            getattr(msg.reply_to, "top_msg_id", None)
            or getattr(msg.reply_to, "reply_to_top_id", None)
        )

    # 2️⃣ Direct topic message
    return getattr(event, "topic_id", None)


@client.on(events.NewMessage(chats=TARGET_GROUP))
async def moderation_handler(event):
    msg = event.message
    if not msg:
        return

    topic_id = resolve_topic_id(event, msg)
    if not topic_id:
        return  # not a forum topic message

    # Exempt bot & anonymous admins
    try:
        if await is_bot_or_anonymous_admin(msg):
            return
    except Exception:
        return

    rules = TOPIC_RULES.get(topic_id)
    if not rules:
        return

    try:
        # =========================
        # 🔁 FORWARDED
        # =========================
        if msg.fwd_from:
            fa = rules.get("forwarded_allowed")

            if fa is False:
                await msg.delete()
                logger.warning("Deleted FORWARDED | topic=%s | user=%s", topic_id, msg.sender_id)
                await send_reason(topic_id, "Forwarded messages are not allowed in this topic.", msg)
                return

            if fa is True:
                return

        # =========================
        # 📝 TEXT
        # =========================
        if msg.text and not msg.media:
            if not rules.get("text", False):
                await msg.delete()
                logger.warning("Deleted TEXT | topic=%s | user=%s", topic_id, msg.sender_id)
                await send_reason(
                    topic_id,
                    "Text messages are not allowed in this topic.\n\n"
                    "👉 Please use [#XFaction-Chat](https://t.me/IngressIN/1)",
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
                logger.warning("Deleted PHOTO | topic=%s | user=%s", topic_id, msg.sender_id)
                await send_reason(topic_id, "Photos are not allowed in this topic.", msg)
            return

        # =========================
        # 🎥 VIDEO
        # =========================
        if msg.video:
            if not rules.get("video", False):
                await msg.delete()
                logger.warning("Deleted VIDEO | topic=%s | user=%s", topic_id, msg.sender_id)
                await send_reason(topic_id, "Videos are not allowed in this topic.", msg)
            return

        # =========================
        # 📦 DOCUMENT
        # =========================
        if isinstance(media, MessageMediaDocument):
            allowed_ext = rules.get("doc_ext")

            if allowed_ext is False:
                await msg.delete()
                logger.warning("Deleted DOCUMENT | topic=%s | user=%s", topic_id, msg.sender_id)
                await send_reason(topic_id, "Documents are not allowed in this topic.", msg)
                return

            if allowed_ext is None:
                return

            filename = msg.file.name or ""
            ext = "." + filename.lower().split(".")[-1] if "." in filename else ""

            if ext not in allowed_ext:
                await msg.delete()
                logger.warning("Deleted DOC %s | topic=%s | user=%s", ext, topic_id, msg.sender_id)
                await send_reason(
                    topic_id,
                    f"File type `{ext}` not allowed.\nAllowed: {', '.join(sorted(allowed_ext))}",
                    msg
                )
            return

    except Exception as e:
        logger.exception("Moderation error: %s", e)
