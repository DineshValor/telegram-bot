from dataclasses import dataclass

@dataclass
class User:
    telegram_id: int
    username: str | None
    is_admin: bool
    is_active: bool
