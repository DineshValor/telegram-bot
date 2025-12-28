import signal
import sys
import asyncio

from core.client import client
from utils.logger import setup_logger


async def shutdown(sig=None):
    """Gracefully shut down the Telegram client."""
    logger = logging.getLogger("telegram-bot")

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
    loop = asyncio.get_event_loop()

    # ✅ Initialize logger WITH event loop (Telegram logging enabled)
    logger = setup_logger(loop)

    logger.info("Starting Telegram bot...")

    # Handle system signals properly
    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(
            sig, lambda s=sig: asyncio.create_task(shutdown(s))
        )

    try:
        client.start()
        logger.info("Telegram bot started successfully")

        # Block until disconnected or shutdown
        client.run_until_disconnected()

    except Exception as e:
        logger.exception("Fatal error: %s", e)
        sys.exit(1)
