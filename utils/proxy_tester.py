from telethon import TelegramClient
from telethon.errors import RPCError

async def test_proxy(api_id, api_hash, proxy):
    try:
        client = TelegramClient(
            "proxy_test",
            api_id,
            api_hash,
            proxy=proxy,
            connection_retries=1
        )

        await client.connect()

        if await client.is_user_authorized():
            await client.disconnect()
            return True

    except Exception:
        pass

    return False
