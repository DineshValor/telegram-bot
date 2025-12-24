#!/usr/bin/env bash
set -e

REPO_DIR="/opt/telegram-bot"
SERVICE="telegram-bot"
BRANCH="master"

cd "$REPO_DIR"

echo "[$(date -u)] Checking for updates..."

git fetch origin

LOCAL=$(git rev-parse HEAD)
REMOTE=$(git rev-parse origin/$BRANCH)

if [ "$LOCAL" != "$REMOTE" ]; then
    echo "Updates found. Pulling..."
    git pull origin $BRANCH
    echo "Restarting bot service..."
    systemctl restart $SERVICE
else
    echo "No updates."
fi
