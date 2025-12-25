#!/bin/bash
set -euo pipefail

REPO_DIR="/opt/telegram-bot"
VENV_DIR="$REPO_DIR/venv"
SERVICE_NAME="telegram-bot"
BRANCH="master"

cd "$REPO_DIR"

echo "[$(date)] 🔍 Checking for updates..."

git fetch origin "$BRANCH"

LOCAL_HASH=$(git rev-parse HEAD)
REMOTE_HASH=$(git rev-parse "origin/$BRANCH")

if [[ "$LOCAL_HASH" == "$REMOTE_HASH" ]]; then
    echo "[$(date)] ✅ No updates found."
    exit 0
fi

echo "[$(date)] ⬇️ Updates detected, pulling..."
git pull --ff-only origin "$BRANCH"

if [[ ! -d "$VENV_DIR" ]]; then
    echo "[$(date)] 🐍 Creating virtual environment..."
    python3 -m venv "$VENV_DIR"
fi

echo "[$(date)] 📦 Updating dependencies..."
"$VENV_DIR/bin/pip" install --upgrade pip
"$VENV_DIR/bin/pip" install -r requirements.txt

echo "[$(date)] 🔄 Restarting bot service..."
systemctl restart "$SERVICE_NAME"

echo "[$(date)] ✅ Update complete."
