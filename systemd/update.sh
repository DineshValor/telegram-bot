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

echo "Fetching latest changes from GitHub..."
git fetch origin "$BRANCH"

LOCAL_HASH=$(git rev-parse HEAD)
REMOTE_HASH=$(git rev-parse "origin/$BRANCH")

# No updates
if [ "$LOCAL_HASH" = "$REMOTE_HASH" ]; then
    echo "No updates found."
    exit 0
fi

echo "Updates found. Replacing tracked files with GitHub version..."

# 🔥 Force replace ONLY tracked files
git reset --hard "origin/$BRANCH"

# 🧹 Remove untracked files ONLY if they block tracked paths
git clean -fd

echo "Restarting service: $SERVICE_NAME"
systemctl restart "$SERVICE_NAME"
