#!/usr/bin/env bash

set -e

REPO_DIR="/home/ubuntu/telegram-bot"
SERVICE_NAME="telegram-bot"
BRANCH="master"

cd "$REPO_DIR"

# Ensure this is a git repo
if [ ! -d ".git" ]; then
    echo "Not a git repository: $REPO_DIR"
    exit 0
fi

# Fetch latest changes
git fetch origin "$BRANCH"

LOCAL_HASH=$(git rev-parse "$BRANCH")
REMOTE_HASH=$(git rev-parse "origin/$BRANCH")

# No updates
if [ "$LOCAL_HASH" = "$REMOTE_HASH" ]; then
    echo "No updates found."
    exit 0
fi

echo "Update found. Pulling changes..."

# 🔴 IMPORTANT CHANGE: catch pull failure
if ! git pull --ff-only origin "$BRANCH"; then
    echo "telegram-bot update failed"
    exit 1
fi

echo "Restarting service: $SERVICE_NAME"
systemctl restart "$SERVICE_NAME"
