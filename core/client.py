from telethon import TelegramClient
from config.env import API_ID, API_HASH, SESSION_NAME

client = TelegramClient(
    SESSION_NAME,
    API_ID,
    API_HASH,
    connection_retries=5,
    retry_delay=5,
    auto_reconnect=True
)
