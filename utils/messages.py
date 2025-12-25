import asyncio
import re

from core.client import client
from config.env import TARGET_GROUP


def escape_md(text: str) -> str:
    """Escape Telegram markdown characters."""
    if not text:
        return ""
    return re.sub(r'([_*`\[\]()])', r'\\\1', text)


async def send_reason(topic_id, reason, offender, ttl=30):
    """
    Send a temporary moderation reason message and auto-delete it.

    :param topic_id: Forum topic ID
    :param reason: Reason text
    :param offender: Original offending message
    :param ttl: Seconds before auto-delete
    """
    mention = "Unknown user"

    try:
        user = await offender.get_sender()
        if user:
            name = escape_md(user.first_name or "User")
            mention = f"[{name}](tg://user?id={user.id})"
    except Exception:
        pass

    try:
        reply = await client.send_message(
            TARGET_GROUP,
            (
                "⚠️ **Message removed**\n"
                f"👤 User: {mention}\n"
                f"📌 Reason: {escape_md(reason)}"
            ),
            reply_to=topic_id,
            parse_mode="md"
        )
    except Exception:
        return

    try:
        await asyncio.sleep(ttl)
        await reply.delete()
    except Exception:
        pass
