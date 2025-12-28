import logging
import asyncio

from utils.telegram_log_handler import TelegramLogHandler


def setup_logger(loop: asyncio.AbstractEventLoop | None = None):
    logger = logging.getLogger("telegram-bot")

    # Always set base level
    logger.setLevel(logging.INFO)

    # Prevent duplicate handlers
    if not any(isinstance(h, TelegramLogHandler) for h in logger.handlers):
        formatter = logging.Formatter(
            "%(levelname)s | %(name)s | %(message)s"
        )

        # Console handler (journalctl)
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        # Telegram handler (ONLY if loop provided)
        if loop is not None:
            tg_handler = TelegramLogHandler(loop)
            tg_handler.setFormatter(formatter)
            logger.addHandler(tg_handler)

    return logger
