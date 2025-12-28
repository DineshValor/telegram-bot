import aiohttp
import asyncio
import sys

from config.env import (
    TELEGRAM_LOG_ENABLED,
    TELEGRAM_LOG_BOT_TOKEN,
    TELEGRAM_LOG_CHAT_ID,
)

API_URL = "https://api.telegram.org/bot{}/sendMessage"


async def send_log(message: str):
    """
    TEMP DEBUG VERSION
    Send a log message to Telegram using Bot API.
    """

    # 🔎 DEBUG 1: function entry
    print("[tg_log] send_log() CALLED", file=sys.stderr)

    if not TELEGRAM_LOG_ENABLED:
        print("[tg_log] TELEGRAM_LOG_ENABLED = False", file=sys.stderr)
        return

    print(
        f"[tg_log] Sending to chat_id={TELEGRAM_LOG_CHAT_ID}",
        file=sys.stderr
    )

    url = API_URL.format(TELEGRAM_LOG_BOT_TOKEN)

    payload = {
        "chat_id": TELEGRAM_LOG_CHAT_ID,
        "text": f"🪵 Bot Log\n\n{message}",
        "disable_web_page_preview": True,
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload, timeout=10) as resp:
                print(
                    f"[tg_log] Telegram API response status: {resp.status}",
                    file=sys.stderr
                )
                text = await resp.text()
                print(
                    f"[tg_log] Telegram API response body: {text}",
                    file=sys.stderr
                )

    except Exception as e:
        print(
            f"[tg_log] EXCEPTION while sending log: {e}",
            file=sys.stderr
        )
