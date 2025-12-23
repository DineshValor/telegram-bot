#!/bin/bash
set -e
cd /home/ubuntu/telegram-bot

git fetch origin main
LOCAL=$(git rev-parse HEAD)
REMOTE=$(git rev-parse origin/main)

if [ "$LOCAL" != "$REMOTE" ]; then
    git pull origin main
    python3 notifier.py "♻️ Bot updated from GitHub"
    systemctl restart telegram-bot.service
fi
