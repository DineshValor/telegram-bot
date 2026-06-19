from telethon import TelegramClient

from telethon.network.connection import (
    ConnectionTcpMTProxyRandomizedIntermediate
)

from config.env import (
    API_ID,
    API_HASH,
    SESSION_NAME,
)

from core.proxy_manager import proxy_manager

_client = None


def create_direct_client():
    return TelegramClient(
        SESSION_NAME,
        API_ID,
        API_HASH,
    )


# ADD BELOW create_direct_client()

def create_mtproto_client(proxy):

    return TelegramClient(
        SESSION_NAME,
        API_ID,
        API_HASH,
        connection=(
            ConnectionTcpMTProxyRandomizedIntermediate
        ),
        proxy=(
            proxy["host"],
            proxy["port"],
            proxy["secret"]
        )
    )


def create_proxy_client():

    proxy = proxy_manager.get_next_proxy()

    if not proxy:
        return None, None

    client = create_mtproto_client(proxy)

    return client, proxy


def get_client():
    global _client

    if _client is None:
        _client = create_direct_client()

    return _client


def set_client(client):
    global _client
    _client = client
