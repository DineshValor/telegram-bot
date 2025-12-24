from telethon import events
from telethon.tl.types import MessageMediaPhoto, MessageMediaDocument

from core.client import client
from config.env import TARGET_GROUP
from config.moderation import TOPIC_RULES
from utils.messages import send_reason
from utils.logger import setup_logger

logger = setup_logger()

@client.on(events.NewMessage(chats=TARGET_GROUP))
async def delete_handler(event):
    msg = event.message

    if not msg or not msg.reply_to:
        return

    me = await client.get_me()
    if msg.from_id and msg.from_id.user_id == me.id:
        return

    topic_id = msg.reply_to.reply_to_msg_id
    rules = TOPIC_RULES.get(topic_id)

    if not rules:
        return

    # 📝 Text
    if msg.text and not msg.media:
        if not rules["text"]:
            await msg.delete()
            logger.warning(
                "Deleted TEXT in topic_id=%s from user_id=%s",
                topic_id,
                msg.sender_id
            )
            await send_reason(
                topic_id,
                (
                    "Text messages are not allowed in this topic.\n\n"
                    "👉 Kindly switch to "
                    "[#XFaction-Chat](https://t.me/IngressIN/1)"
                ),
                msg
            )
        return

    media = msg.media

    # 🖼 Photo
    if isinstance(media, MessageMediaPhoto):
        if not rules["photo"]:
            await msg.delete()
            logger.warning(
                "Deleted PHOTO in topic_id=%s from user_id=%s",
                topic_id,
                msg.sender_id
            )
            await send_reason(topic_id, "Photos are not allowed here.", msg)
        return

    # 🎥 Video
    if msg.video:
        if not rules["video"]:
            await msg.delete()
            logger.warning(
                "Deleted VIDEO in topic_id=%s from user_id=%s",
                topic_id,
                msg.sender_id
            )
            await send_reason(topic_id, "Videos are not allowed here.", msg)
        return

    # 📦 Document
    if isinstance(media, MessageMediaDocument) and not msg.video:
        filename = msg.file.name or "unknown"
        ext = "." + filename.lower().split(".")[-1] if "." in filename else ""

        if ext not in rules["doc_ext"]:
            await msg.delete()
            logger.warning(
                "Deleted DOCUMENT (%s) in topic_id=%s from user_id=%s",
                ext,
                topic_id,
                msg.sender_id
            )
            allowed = ", ".join(sorted(rules["doc_ext"]))
            await send_reason(
                topic_id,
                f"File type `{ext}` not allowed.\nAllowed: {allowed}",
                msg
        )
