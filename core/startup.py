import signal
import sys
import asyncio

from core.client import client
from utils.logger import setup_logger

from utils.proxy_manager import fetch_proxies
from utils.proxy_tester import test_proxy
from telethon import TelegramClient
from config.env import API_ID, API_HASH, SESSION_NAME

logger = setup_logger()


async def shutdown(sig=None):
    """Gracefully shut down the Telegram client."""
    if sig:
        logger.warning("Received signal %s, shutting down...", sig.name)

    try:
        await client.disconnect()
        logger.info("Telegram client disconnected cleanly")
    except Exception as e:
        logger.exception("Error during shutdown: %s", e)

    # Stop the asyncio loop cleanly
    loop = asyncio.get_running_loop()
    loop.stop()


def start_bot():
    logger.info("Starting Telegram bot...")

    loop = asyncio.get_event_loop()

    # Handle system signals properly
    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(
            sig, lambda s=sig: asyncio.create_task(shutdown(s))
        )

    try:
    client.start()
    logger.info("Connected directly")

except Exception:
    logger.warning("Direct connection failed")

    proxies = fetch_proxies()

    for proxy in proxies:

        try:
            if loop.run_until_complete(
                test_proxy(
                    API_ID,
                    API_HASH,
                    proxy
                )
            ):

                logger.info(
                    f"Using proxy {proxy}"
                )

                proxy_client = TelegramClient(
                    SESSION_NAME,
                    API_ID,
                    API_HASH,
                    proxy=proxy,
                    auto_reconnect=True
                )

                proxy_client.start()

                globals()["client"] = proxy_client

                break

        except Exception:
            continue

logger.info("Telegram bot started successfully")
client.run_until_disconnected()

    except Exception as e:
        logger.exception("Fatal error: %s", e)
        sys.exit(1)
