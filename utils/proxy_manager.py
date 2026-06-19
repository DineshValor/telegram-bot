import json
import requests
from pathlib import Path
from urllib.parse import urlparse, parse_qs

PROXY_FILE = "proxy_cache.json"

PROXY_SOURCE = (
    "https://raw.githubusercontent.com/"
    "SoliSpirit/mtproto/refs/heads/master/all_proxies.txt"
)

def load_cached_proxy():
    if Path(PROXY_FILE).exists():
        with open(PROXY_FILE, "r") as f:
    return json.load(f)
    return None

def save_proxy(proxy):
    with open(PROXY_FILE, "w") as f:
    json.dump(proxy, f)

def fetch_proxies():
    r = requests.get(PROXY_SOURCE, timeout=30)
    r.raise_for_status()

    proxies = []

    for line in r.text.splitlines():
        line = line.strip()

        if not line:
            continue

        try:
            parsed = parse_qs(urlparse(line).query)

            proxies.append({
                "server": parsed["server"][0],
                "port": int(parsed["port"][0]),
                "secret": parsed["secret"][0]
            })

        except Exception:
            continue

    return proxies
