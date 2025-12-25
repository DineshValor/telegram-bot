#!/bin/bash
set -e

REPO_DIR="/opt/telegram-bot"
VENV_DIR="$REPO_DIR/venv"
SERVICE_NAME="telegrambot"   # ⚠ must match systemd filename
BRANCH="master"

cd "$REPO_DIR"

echo "[$(date)] Checking for updates..."

git fetch origin

LOCAL=$(git rev-parse HEAD)
REMOTE=$(git rev-parse origin/$BRANCH)

if [ "$LOCAL" != "$REMOTE" ]; then
    echo "[$(date)] Updates found. Pulling..."
    git pull origin $BRANCH

    # Create venv if missing
    if [ ! -d "$VENV_DIR" ]; then
        echo "[$(date)] Virtualenv not found. Creating..."
        python3 -m venv "$VENV_DIR"
    fi

    echo "[$(date)] Installing dependencies..."
    "$VENV_DIR/bin/pip" install --upgrade pip
    "$VENV_DIR/bin/pip" install -r requirements.txt

    echo "[$(date)] Restarting service..."
    systemctl restart "$SERVICE_NAME"
else
    echo "[$(date)] No updates."
fi
