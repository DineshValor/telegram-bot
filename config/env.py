import os

def get_env(key: str, required: bool = True, default=None):
    value = os.getenv(key, default)
    if required and value is None:
        raise RuntimeError(f"Missing required env variable: {key}")
    return value

BOT_TOKEN = get_env("BOT_TOKEN")
API_ID = int(get_env("API_ID"))
API_HASH = get_env("API_HASH")
