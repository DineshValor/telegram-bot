from telethon import TelegramClient


async def test_proxy(api_id, api_hash, proxy):
    client = None

    try:
        client = TelegramClient(
            "proxy_test",
            api_id,
            api_hash,
            proxy=(
                proxy["server"],
                proxy["port"],
                proxy["secret"]
            ),
            connection_retries=1
        )

        await client.connect()

        return client.is_connected()

    except Exception:
        return False

    finally:
        try:
            if client:
                await client.disconnect()
        except Exception:
            pass
