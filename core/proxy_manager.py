import aiohttp
import asyncio
import json
from pathlib import Path

PROXY_SOURCE = (
    "https://raw.githubusercontent.com/SoliSpirit/mtproto/master/all_proxies.txt"
)

CACHE_FILE = Path("data/mtproto_cache.json")


async def fetch_proxy_list():
    async with aiohttp.ClientSession() as session:
        async with session.get(PROXY_SOURCE, timeout=30) as response:
            text = await response.text()

    proxies = []

    for line in text.splitlines():
        line = line.strip()

        if not line:
            continue

        try:
            host, port, secret = line.split(":")
            proxies.append(
                {
                    "host": host,
                    "port": int(port),
                    "secret": secret,
                }
            )
        except Exception:
            continue

    return proxies


def save_cache(proxies):
    CACHE_FILE.parent.mkdir(exist_ok=True)

    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(proxies, f)


def load_cache():
    if not CACHE_FILE.exists():
        return []

    with open(CACHE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)
