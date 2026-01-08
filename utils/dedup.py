import time
import hashlib

DEDUP_CACHE = {}
TTL_SECONDS = 3600  # 1 hour


def _cleanup():
    now = time.time()
    for k, ts in list(DEDUP_CACHE.items()):
        if now - ts > TTL_SECONDS:
            del DEDUP_CACHE[k]


def make_fingerprint(msg):
    parts = []

    if msg.text:
        parts.append(msg.text)

    if msg.media:
        parts.append(str(type(msg.media)))

        if msg.file:
            parts.append(msg.file.id or "")
            parts.append(str(msg.file.size or ""))

    raw = "|".join(parts)
    return hashlib.sha256(raw.encode()).hexdigest()


def seen_before(topic_id, fingerprint):
    _cleanup()
    key = (topic_id, fingerprint)
    if key in DEDUP_CACHE:
        return True

    DEDUP_CACHE[key] = time.time()
    return False
