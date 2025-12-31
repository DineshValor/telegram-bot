#!/bin/bash
set -euo pipefail

ENV_FILE="/home/ubuntu/telegram-bot/.env"

# =========================
# Load .env safely
# =========================
if [ ! -f "$ENV_FILE" ]; then
    echo "Env file not found: $ENV_FILE" >&2
    exit 1
fi

# Export variables from .env
set -a
source "$ENV_FILE"
set +a

# =========================
# Required variables check
# =========================
: "${TELEGRAM_LOG_BOT_TOKEN:?Missing TELEGRAM_LOG_BOT_TOKEN}"
: "${TELEGRAM_LOG_CHAT_ID:?Missing TELEGRAM_LOG_CHAT_ID}"

BOT_TOKEN="$TELEGRAM_LOG_BOT_TOKEN"
CHAT_ID="$TELEGRAM_LOG_CHAT_ID"

API_URL="https://api.telegram.org/bot${BOT_TOKEN}/sendMessage"

send_msg() {
    local text="$1"
    curl -s -X POST "$API_URL" \
        -d chat_id="$CHAT_ID" \
        -d disable_web_page_preview=true \
        -d text="$text" >/dev/null
}

journalctl -f -o cat \
    -u telegram-bot.service \
    -u telegram-bot-update.service \
    -u telegram-bot-failure.service |
while read -r line; do

    if echo "$line" | grep -qx "telegram-bot started"; then
        send_msg "▶️ telegram-bot started"
    fi

    if echo "$line" | grep -qx "telegram-bot stopped"; then
        send_msg "🛑 telegram-bot stopped"
    fi

    if echo "$line" | grep -qx "telegram-bot crashed"; then
        send_msg "❌ telegram-bot crashed"
    fi

    if echo "$line" | grep -q "Restarting service: telegram-bot"; then
        send_msg "🔄 telegram-bot updated"
    fi

done
