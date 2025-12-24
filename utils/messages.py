import asyncio
from core.client import client
from config.env import TARGET_GROUP

async def send_reason(topic_id, reason, offender, ttl=30):
    mention = "Unknown user"

    try:
        user = await offender.get_sender()
        if user:
            mention = f"[{user.first_name}](tg://user?id={user.id})"
    except Exception:
        pass

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

    await asyncio.sleep(ttl)
    await reply.delete()
