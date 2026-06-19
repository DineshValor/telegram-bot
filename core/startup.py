import signal
import sys
import asyncio

from core.client import (
    get_client,
    connect_with_fallback,
)

from core.proxy_manager import (
    proxy_manager
)

from utils.logger import setup_logger

logger = setup_logger()


async def shutdown(sig=None):
    """Gracefully shut down the Telegram client."""

    if sig:
        logger.warning(
            "Received signal %s, shutting down...",
            sig.name
        )

    try:
        client = get_client()

        await client.disconnect()

        logger.info(
            "Telegram client disconnected cleanly"
        )

    except Exception as e:
        logger.exception(
            "Error during shutdown: %s",
            e
        )

    loop = asyncio.get_running_loop()
    loop.stop()


def start_bot():

    logger.info(
        "Starting Telegram bot..."
    )

    loop = asyncio.get_event_loop()

    #
    # Signal handlers
    #
    for sig in (
        signal.SIGINT,
        signal.SIGTERM
    ):
        loop.add_signal_handler(
            sig,
            lambda s=sig:
            asyncio.create_task(
                shutdown(s)
            )
        )

    try:

        #
        # Load cached proxies
        #
        proxy_manager.load_cache()

        #
        # Start 12h refresh task
        #
        loop.create_task(
            proxy_manager.refresh_loop()
        )

        #
        # Direct → MTProto fallback
        #
        client = loop.run_until_complete(
            connect_with_fallback()
        )

        logger.info(
            "Telegram bot started successfully"
        )

        client.run_until_disconnected()

    except Exception as e:

        logger.exception(
            "Fatal error: %s",
            e
        )

        sys.exit(1)
