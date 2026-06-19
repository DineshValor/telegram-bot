from telethon import TelegramClient
from telethon.errors import RPCError

async def test_proxy(api_id, api_hash, proxy):

    try:
        client = TelegramClient(
            "proxy_test",
            api_id,
            api_hash,
            proxy=(
                proxy["server"],
                proxy["port"],
                proxy["secret"]
            )
        )

        await client.connect()

        ok = await client.is_user_authorized()

        await client.disconnect()

        return ok

    except Exception:
        return False
