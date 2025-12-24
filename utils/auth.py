import json
from pathlib import Path

AUTH_FILE = Path("authorized_users.json")

def _load():
    if not AUTH_FILE.exists():
        return {"admins": [], "users": []}

    with open(AUTH_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def _save(data):
    with open(AUTH_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def is_admin(user_id: int) -> bool:
    data = _load()
    return user_id in data.get("admins", [])

def is_authorized(user_id: int) -> bool:
    data = _load()
    return user_id in data.get("users", []) or is_admin(user_id)

def add_user(user_id: int):
    data = _load()
    if user_id not in data["users"]:
        data["users"].append(user_id)
        _save(data)
