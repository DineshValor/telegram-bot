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


def _make_fingerprint(msg):
    parts = []

    # 1️⃣ Visible text (most reliable)
    if msg.raw_text:
        parts.append(msg.raw_text.strip())
    elif msg.text:
        parts.append(msg.text.strip())

    # 2️⃣ Media type + size (SAFE across all media)
    if msg.media:
        parts.append(type(msg.media).__name__)

        if msg.file:
            if msg.file.size:
                parts.append(str(msg.file.size))

            # Fallbacks (safe attributes)
            if msg.file.name:
                parts.append(msg.file.name)

    raw = "|".join(parts)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()

def is_duplicate_new_post(fingerprint):
    _cleanup()

    if fingerprint in SEEN_CONTENT:
        return True

    SEEN_CONTENT[fingerprint] = time.time()
    return False
