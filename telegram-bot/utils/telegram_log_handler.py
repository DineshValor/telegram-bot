import logging
import asyncio

from utils.tg_log import send_log
from config.env import TELEGRAM_LOG_ENABLED, TELEGRAM_LOG_LEVEL


class TelegramLogHandler(logging.Handler):
    def __init__(self, loop: asyncio.AbstractEventLoop):
        super().__init__()
        self.loop = loop
        self.setLevel(getattr(logging, TELEGRAM_LOG_LEVEL, logging.ERROR))

    def emit(self, record: logging.LogRecord):
        if not TELEGRAM_LOG_ENABLED:
            return

        try:
            msg = self.format(record)

            # Never block logging
            self.loop.create_task(
                send_log(msg)
            )
        except Exception:
            pass
