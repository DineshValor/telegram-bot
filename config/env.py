import os
from dotenv import load_dotenv

load_dotenv()

# =========================
# Telegram userbot config
# =========================
API_ID = int(os.getenv("API_ID", "0"))
API_HASH = os.getenv("API_HASH")
SESSION_NAME = os.getenv("SESSION_NAME", "user_session")
TARGET_GROUP = int(os.getenv("TARGET_GROUP", "0"))

if not API_ID or not API_HASH:
    raise RuntimeError("❌ API_ID or API_HASH missing in .env")

# =========================
# Telegram logging (Bot API)
# =========================
TELEGRAM_LOG_ENABLED = os.getenv("TELEGRAM_LOG_ENABLED", "false").lower() == "true"
TELEGRAM_LOG_BOT_TOKEN = os.getenv("TELEGRAM_LOG_BOT_TOKEN")
TELEGRAM_LOG_CHAT_ID = os.getenv("TELEGRAM_LOG_CHAT_ID")

if TELEGRAM_LOG_ENABLED:
    if not TELEGRAM_LOG_BOT_TOKEN or not TELEGRAM_LOG_CHAT_ID:
        raise RuntimeError("❌ Telegram log bot config missing in .env")
