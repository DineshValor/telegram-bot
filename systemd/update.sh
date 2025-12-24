#!/bin/bash
set -e

REPO_DIR="/opt/telegram-bot"
SERVICE_NAME="telegram-bot"
BRANCH="master"

cd "$REPO_DIR"

echo "[$(date)] Checking for updates..."

# Fetch latest changes
git fetch origin

LOCAL=$(git rev-parse HEAD)
REMOTE=$(git rev-parse origin/$BRANCH)

if [ "$LOCAL" != "$REMOTE" ]; then
    echo "[$(date)] Updates found. Pulling..."
    git pull origin $BRANCH

    echo "[$(date)] Restarting service..."
    systemctl restart $SERVICE_NAME
else
    echo "[$(date)] No updates."
fi
