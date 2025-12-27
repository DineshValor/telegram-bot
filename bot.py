from core.startup import start_bot
from utils.logger import get_logger

logger = get_logger(__name__)

if __name__ == "__main__":
    try:
        start_bot()
    except Exception as e:
        logger.exception("Bot failed to start")
