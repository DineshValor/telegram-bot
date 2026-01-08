import hashlib
import time

# fingerprint -> timestamp
SEEN_CONTENT = {}

TTL_SECONDS = 6 * 60 * 60  # 6 hours (tune as needed)


def _cleanup():
    now = time.time()
    for fp, ts in list(SEEN_CONTENT.items()):
        if now - ts > TTL_SECONDS:
            del SEEN_CONTENT[fp]


def make_fingerprint(msg):
    parts = []

    if msg.text:
        parts.append(msg.text.strip())

    if msg.media:
        parts.append(type(msg.media).__name__)

        if msg.file:
            parts.append(str(msg.file.size or ""))
            parts.append(str(msg.file.id or ""))

    raw = "|".join(parts)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def is_duplicate_new_post(fingerprint):
    _cleanup()

    if fingerprint in SEEN_CONTENT:
        return True

    SEEN_CONTENT[fingerprint] = time.time()
    return False
