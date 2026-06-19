import json
import requests
from pathlib import Path

PROXY_FILE = "proxy_cache.json"

PROXY_SOURCE = (
    "https://raw.githubusercontent.com/"
    "SoliSpirit/mtproto/main/proxies.json"
)

def load_cached_proxy():
    if Path(PROXY_FILE).exists():
        return json.load(open(PROXY_FILE))
    return None

def save_proxy(proxy):
    json.dump(proxy, open(PROXY_FILE, "w"))

def fetch_proxies():
    r = requests.get(PROXY_SOURCE, timeout=30)
    r.raise_for_status()
    return r.json()
