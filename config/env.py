import os
from dotenv import load_dotenv

load_dotenv()

# =========================
# Telegram userbot config
# =========================
API_ID = int(os.getenv("API_ID", "0"))
API_HASH = os.getenv("API_HASH")
SESSION_NAME = os.getenv("SESSION_NAME", "user_session")

TARGET_GROUP_RAW = os.getenv("TARGET_GROUP")
if not TARGET_GROUP_RAW:
    raise RuntimeError("❌ TARGET_GROUP missing in .env")

TARGET_GROUP = int(TARGET_GROUP_RAW)

if not API_ID or not API_HASH:
    raise RuntimeError("❌ API_ID or API_HASH missing in .env")

# =========================
# Telegram logging (Bot API)
# =========================
TELEGRAM_LOG_ENABLED = os.getenv("TELEGRAM_LOG_ENABLED", "false").lower() == "true"

TELEGRAM_LOG_BOT_TOKEN = None
TELEGRAM_LOG_CHAT_ID = None

if TELEGRAM_LOG_ENABLED:
    TELEGRAM_LOG_BOT_TOKEN = os.getenv("TELEGRAM_LOG_BOT_TOKEN")
    TELEGRAM_LOG_CHAT_ID_RAW = os.getenv("TELEGRAM_LOG_CHAT_ID")

    if not TELEGRAM_LOG_BOT_TOKEN or not TELEGRAM_LOG_CHAT_ID_RAW:
        raise RuntimeError("❌ Telegram log bot config missing in .env")

    TELEGRAM_LOG_CHAT_ID = int(TELEGRAM_LOG_CHAT_ID_RAW)

    if TELEGRAM_LOG_CHAT_ID == 0:
        raise RuntimeError("❌ TELEGRAM_LOG_CHAT_ID cannot be 0")
