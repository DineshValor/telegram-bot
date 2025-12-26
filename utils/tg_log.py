import aiohttp
import asyncio

from config.env import (
    TELEGRAM_LOG_ENABLED,
    TELEGRAM_LOG_BOT_TOKEN,
    TELEGRAM_LOG_CHAT_ID,
)

API_URL = "https://api.telegram.org/bot{}/sendMessage"


async def send_log(message: str):
    """
    Send a log message to Telegram using Bot API.
    Never crashes the bot.
    Never writes to disk.
    """
    if not TELEGRAM_LOG_ENABLED:
        return

    url = API_URL.format(TELEGRAM_LOG_BOT_TOKEN)

    payload = {
        "chat_id": TELEGRAM_LOG_CHAT_ID,
        "text": f"🪵 Bot Log\n\n{message}",
        "disable_web_page_preview": True,
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload, timeout=10):
                pass
    except Exception:
        # Logging must NEVER break the bot
        pass
