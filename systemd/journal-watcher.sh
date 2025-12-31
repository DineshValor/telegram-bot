#!/bin/bash

# ========= CONFIG =========
BOT_TOKEN="YOUR_TELEGRAM_BOT_TOKEN"
CHAT_ID="YOUR_TELEGRAM_CHAT_ID"

SERVICE_NAME="telegram-bot.service"
UPDATE_SERVICE="telegram-bot-update.service"

API_URL="https://api.telegram.org/bot${BOT_TOKEN}/sendMessage"

send_msg() {
    local text="$1"
    curl -s -X POST "$API_URL" \
        -d chat_id="$CHAT_ID" \
        -d disable_web_page_preview=true \
        -d text="$text" >/dev/null
}

journalctl -f -o cat \
    -u "$SERVICE_NAME" \
    -u "$UPDATE_SERVICE" |
while read -r line; do

    if echo "$line" | grep -q "Started Telegram bot"; then
        send_msg "▶️ telegram-bot started"
    fi

    if echo "$line" | grep -q "Stopping Telegram bot"; then
        send_msg "🛑 telegram-bot stopped"
    fi

    if echo "$line" | grep -Eq "Failed with result|Main process exited"; then
        send_msg "❌ telegram-bot crashed or failed"
    fi

    if echo "$line" | grep -q "Restarting service: telegram-bot"; then
        send_msg "🔄 telegram-bot updated & restarted"
    fi

done
