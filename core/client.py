from telethon import TelegramClient

from config.env import (
    API_ID,
    API_HASH,
    SESSION_NAME,
)

_client = None


def create_direct_client():
    return TelegramClient(
        SESSION_NAME,
        API_ID,
        API_HASH,
    )


def get_client():
    global _client

    if _client is None:
        _client = create_direct_client()

    return _client


def set_client(client):
    global _client
    _client = client
