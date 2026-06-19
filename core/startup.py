import signal
import sys
import asyncio

from telethon import TelegramClient

from core.client import client
from config.env import API_ID, API_HASH, SESSION_NAME
from utils.logger import setup_logger

from utils.proxy_manager import (
    fetch_proxies,
    save_proxy,
    load_cached_proxy
)

from utils.proxy_tester import test_proxy

logger = setup_logger()


async def shutdown(sig=None):
    """Gracefully shut down the Telegram client."""
    if sig:
        logger.warning(
            "Received signal %s, shutting down...",
            sig.name
        )

    try:
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

    logger.info("Starting Telegram bot...")

    loop = asyncio.get_event_loop()

    # Handle system signals
    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(
            sig,
            lambda s=sig: asyncio.create_task(
                shutdown(s)
            )
        )

    active_client = client

    # ==================================================
    # Try cached proxy first
    # ==================================================

    cached_proxy = load_cached_proxy()

    if cached_proxy:

        try:
            logger.info(
                "Trying cached proxy %s:%s",
                cached_proxy["server"],
                cached_proxy["port"]
            )

            active_client = TelegramClient(
                SESSION_NAME,
                API_ID,
                API_HASH,
                proxy=(
                    cached_proxy["server"],
                    cached_proxy["port"],
                    cached_proxy["secret"]
                ),
                auto_reconnect=True,
                connection_retries=5,
                retry_delay=5
            )

            active_client.start()

            logger.info(
                "Connected using cached proxy"
            )

            active_client.run_until_disconnected()
            return

        except Exception as e:

            logger.warning(
                "Cached proxy failed: %s",
                str(e)
            )

    # ==================================================
    # Try direct connection
    # ==================================================

    try:

        active_client.start()

        logger.info(
            "Connected directly"
        )

    except Exception as e:

        logger.warning(
            "Direct connection failed: %s",
            str(e)
        )

        # ==============================================
        # Fetch and test proxies
        # ==============================================

        try:

            proxies = fetch_proxies()

            logger.info(
                "Fetched %s proxies",
                len(proxies)
            )

            # Limit startup testing
            proxies = proxies[:100]

            for proxy in proxies:

                try:

                    working = loop.run_until_complete(
                        test_proxy(
                            API_ID,
                            API_HASH,
                            proxy
                        )
                    )

                    if not working:
                        continue

                    logger.info(
                        "Working proxy found: %s:%s",
                        proxy["server"],
                        proxy["port"]
                    )

                    active_client = TelegramClient(
                        SESSION_NAME,
                        API_ID,
                        API_HASH,
                        proxy=(
                            proxy["server"],
                            proxy["port"],
                            proxy["secret"]
                        ),
                        auto_reconnect=True,
                        connection_retries=5,
                        retry_delay=5
                    )

                    active_client.start()

                    save_proxy(proxy)

                    logger.info(
                        "Connected using proxy"
                    )

                    break

                except Exception as proxy_error:

                    logger.warning(
                        "Proxy failed: %s",
                        str(proxy_error)
                    )

                    continue

        except Exception as proxy_fetch_error:

            logger.exception(
                "Failed to fetch/test proxies: %s",
                proxy_fetch_error
            )

            sys.exit(1)

    # ==================================================
    # Start bot
    # ==================================================

    try:

        logger.info(
            "Telegram bot started successfully"
        )

        active_client.run_until_disconnected()

    except Exception as e:

        logger.exception(
            "Fatal error: %s",
            e
        )

        sys.exit(1)
