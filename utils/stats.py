from collections import defaultdict
from threading import Lock

_lock = Lock()

_stats = {
    "forwarded": 0,
    "deleted": 0,
    "per_topic": defaultdict(int),
}

def inc_forwarded(topic_id: int):
    with _lock:
        _stats["forwarded"] += 1
        _stats["per_topic"][topic_id] += 1

def inc_deleted(topic_id: int):
    with _lock:
        _stats["deleted"] += 1
        _stats["per_topic"][topic_id] += 1

def get_stats():
    with _lock:
        return {
            "forwarded": _stats["forwarded"],
            "deleted": _stats["deleted"],
            "per_topic": dict(_stats["per_topic"]),
        }
