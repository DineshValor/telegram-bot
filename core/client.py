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


async def connect_with_fallback():

    #
    # Try direct connection first
    #
    try:

        client = create_direct_client()

        await client.connect()

        if await client.is_user_authorized():

            print(
                "[CLIENT] Direct connection established"
            )

            set_client(client)

            return client

        await client.disconnect()

    except Exception as e:

        print(
            f"[CLIENT] Direct connection failed: {e}"
        )

    #
    # Fallback to MTProto proxies
    #
    while True:

        client, proxy = create_proxy_client()

        if not client:
            raise RuntimeError(
                "No usable MTProto proxies available"
            )

        try:

            print(
                "[CLIENT] Trying proxy "
                f"{proxy['host']}:{proxy['port']}"
            )

            await client.connect()

            if await client.is_user_authorized():

                print(
                    "[CLIENT] Connected via MTProto "
                    f"{proxy['host']}:{proxy['port']}"
                )

                set_client(client)

                return client

            await client.disconnect()

            proxy_manager.mark_failed(proxy)

        except Exception:

            proxy_manager.mark_failed(proxy)

            try:
                await client.disconnect()
            except Exception:
                pass

            continue


def get_client():
    global _client

    if _client is None:
        _client = create_direct_client()

    return _client


def set_client(client):
    global _client
    _client = client


# Backward compatibility
client = get_client())
