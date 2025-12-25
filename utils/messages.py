import asyncio
import re

from core.client import client
from config.env import TARGET_GROUP


def escape_md(text: str) -> str:
    """Escape Telegram markdown characters (for user-generated text only)."""
    if not text:
        return ""
    return re.sub(r'([_*`\[\]()])', r'\\\1', text)


async def send_reason(topic_id, reason, offender, ttl=30):
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
                f"📌 Reason: {reason}"
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
