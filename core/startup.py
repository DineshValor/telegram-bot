from core.client import client
from utils.logger import setup_logger

logger = setup_logger()

def start_bot():
    logger.info("Bot starting...")
    client.start()
    logger.info("Bot started successfully")
    client.run_until_disconnected()
