import asyncio
import aiohttp
import time
from pathlib import Path

PROXY_URL = (
    "https://raw.githubusercontent.com/"
    "SoliSpirit/mtproto/master/all_proxies.txt"
)

CACHE_FILE = Path("data/mtproto_proxies.txt")

REFRESH_INTERVAL = 12 * 60 * 60
MAX_FAILS = 3


class ProxyManager:
    def __init__(self):
        self.proxies = []
        self.current_index = 0

        # proxy_key -> fail_count
        self.fail_counts = {}

        self.last_refresh = 0

    async def refresh(self):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    PROXY_URL,
                    timeout=30
                ) as resp:

                    if resp.status != 200:
                        return False

                    text = await resp.text()

            CACHE_FILE.parent.mkdir(
                parents=True,
                exist_ok=True
            )

            CACHE_FILE.write_text(
                text,
                encoding="utf-8"
            )

            self._parse(text)

            self.last_refresh = time.time()

            print(
                f"[PROXY] Refreshed "
                f"{len(self.proxies)} proxies"
            )

            return True

        except Exception as e:
            print(
                f"[PROXY] Refresh failed: {e}"
            )
            return False

    def load_cache(self):
        if not CACHE_FILE.exists():
            return False

        try:
            text = CACHE_FILE.read_text(
                encoding="utf-8"
            )

            self._parse(text)

            print(
                f"[PROXY] Loaded "
                f"{len(self.proxies)} cached proxies"
            )

            return True

        except Exception as e:
            print(
                f"[PROXY] Cache load failed: {e}"
            )
            return False

    def _parse(self, text):
        proxies = []

        for line in text.splitlines():

            line = line.strip()

            if not line:
                continue

            parts = line.split(":")

            if len(parts) < 3:
                continue

            try:
                proxies.append(
                    {
                        "host": parts[0],
                        "port": int(parts[1]),
                        "secret": parts[2],
                    }
                )
            except Exception:
                continue

        self.proxies = proxies
        self.current_index = 0

        #
        # CLEANUP EVERY REFRESH
        #
        self.fail_counts.clear()

    def mark_dead(self, proxy):
        key = (
            proxy["host"],
            proxy["port"],
            proxy["secret"]
        )

        self.fail_counts[key] = (
            self.fail_counts.get(key, 0) + 1
        )

    def get_fail_count(self, proxy):
        key = (
            proxy["host"],
            proxy["port"],
            proxy["secret"]
        )

        return self.fail_counts.get(key, 0)

    def get_next_proxy(self):
        if not self.proxies:
            return None

        total = len(self.proxies)

        for _ in range(total):

            proxy = self.proxies[
                self.current_index % total
            ]

            self.current_index += 1

            fails = self.get_fail_count(
                proxy
            )

            if fails < MAX_FAILS:
                return proxy

        return None

    async def refresh_loop(self):
        while True:

            await self.refresh()

            await asyncio.sleep(
                REFRESH_INTERVAL
            )


proxy_manager = ProxyManager()
