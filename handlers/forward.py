import asyncio
import re
import hashlib
import time

from telethon import events
from telethon.errors import FloodWaitError
from telethon.tl.types import (
    MessageMediaPhoto,
    MessageMediaDocument,
    MessageMediaWebPage,
    MessageEntityUrl,
    MessageEntityTextUrl,
)

from core.client import client
from config.env import TARGET_GROUP
from config.forwarding import (
    CHANNEL_TOPIC_MAP,
    FORWARD_TOPIC_RULES,
    DEDUP_TOPIC_RULES,
)
from utils.logger import setup_logger

logger = setup_logger()

FORWARDED_MAP = {}

URL_RE = re.compile(r"https?://\S+", re.IGNORECASE)

# =========================
# Dedup store (in-memory)
# =========================

DEDUP_CACHE = {}  # (topic_id, fingerprint) -> timestamp
DEDUP_TTL = 6 * 60 * 60  # 6 hours


def _dedup_cleanup():
    now = time.time()
    for k, ts in list(DEDUP_CACHE.items()):
        if now - ts > DEDUP_TTL:
            del DEDUP_CACHE[k]


def _make_fingerprint(msg):
    parts = []

    # Visible content
    if msg.raw_text:
        parts.append(msg.raw_text.strip())
    elif msg.text:
        parts.append(msg.text.strip())

    # Media identity
    if msg.media:
        parts.append(type(msg.media).__name__)
        if msg.file:
            parts.append(str(msg.file.id or ""))
            parts.append(str(msg.file.size or ""))

    raw = "|".join(parts)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


# =========================
# Helpers
# =========================

def _is_raw_link_only(msg):
    if not msg.raw_text:
        return False
    return bool(URL_RE.fullmatch(msg.raw_text.strip()))


def allowed_by_topic_rules(msg, topic_id):
    rules = FORWARD_TOPIC_RULES.get(topic_id)

    if not rules:
        return True

    if isinstance(msg.media, MessageMediaWebPage):
        return rules.get("link", rules.get("text", False))

    if msg.entities:
        for ent in msg.entities:
            if not isinstance(ent, (MessageEntityUrl, MessageEntityTextUrl)):
                break
        else:
            return rules.get("link", rules.get("text", False))

    if not msg.media and not msg.text and _is_raw_link_only(msg):
        return rules.get("link", rules.get("text", False))

    if msg.text and not msg.media:
        return rules.get("text", False)

    media = msg.media

    if isinstance(media, MessageMediaPhoto):
        return rules.get("photo", False)

    if msg.video:
        return rules.get("video", False)

    if isinstance(media, MessageMediaDocument):
        allowed = rules.get("doc_ext")
        if allowed is None:
            return True

        filename = msg.file.name or ""
        ext = "." + filename.lower().split(".")[-1] if "." in filename else ""
        return ext in allowed

    return False


# =========================
# Forwarding
# =========================

async def safe_forward(msg, topic_id):
    try:
        fwd = await client.send_message(
            TARGET_GROUP,
            msg,
            reply_to=topic_id
        )
        FORWARDED_MAP[msg.id] = fwd.id
        return fwd

    except FloodWaitError as e:
        logger.warning("FloodWait %ss — sleeping", e.seconds)
        await asyncio.sleep(e.seconds)
        return await safe_forward(msg, topic_id)

    except Exception as e:
        logger.exception("Forward failed: %s", e)
        return None


# =========================
# New message handler
# =========================

@client.on(events.NewMessage(chats=list(CHANNEL_TOPIC_MAP.keys())))
async def forward_handler(event):
    msg = event.message
    topic_id = CHANNEL_TOPIC_MAP.get(event.chat_id)

    if not msg or not topic_id:
        return

    if not allowed_by_topic_rules(msg, topic_id):
        logger.info(
            "SKIP topic_rules msg_id=%s topic=%s",
            msg.id,
            topic_id
        )
        return

    dedup_cfg = DEDUP_TOPIC_RULES.get(topic_id)
    if dedup_cfg and dedup_cfg.get("dedup_new"):
        _dedup_cleanup()
        fp = _make_fingerprint(msg)
        key = (topic_id, fp)

        if key in DEDUP_CACHE:
            logger.info(
                "SKIP dedup_new topic=%s msg_id=%s",
                topic_id,
                msg.id
            )
            return

        DEDUP_CACHE[key] = time.time()

    await safe_forward(msg, topic_id)


# =========================
# Album handler (unchanged)
# =========================

@client.on(events.Album(chats=list(CHANNEL_TOPIC_MAP.keys())))
async def album_handler(event):
    topic_id = CHANNEL_TOPIC_MAP.get(event.chat_id)

    if not topic_id:
        return

    for msg in event.messages:
        if not allowed_by_topic_rules(msg, topic_id):
            return

    try:
        fwd_msgs = await client.send_message(
            TARGET_GROUP,
            event.messages,
            reply_to=topic_id
        )

        for src, fwd in zip(event.messages, fwd_msgs):
            FORWARDED_MAP[src.id] = fwd.id

    except Exception as e:
        logger.exception("Album forward failed: %s", e)


# =========================
# Edit handler (stock + optional strict dedup)
# =========================

@client.on(events.MessageEdited(chats=list(CHANNEL_TOPIC_MAP.keys())))
async def edit_handler(event):
    msg = event.message
    topic_id = CHANNEL_TOPIC_MAP.get(event.chat_id)

    if not msg or not topic_id:
        return

    old_fwd = FORWARDED_MAP.pop(msg.id, None)

    try:
        if old_fwd:
            await client.delete_messages(TARGET_GROUP, old_fwd)

        if not allowed_by_topic_rules(msg, topic_id):
            logger.info(
                "SKIP edit_topic_rules msg_id=%s topic=%s",
                msg.id,
                topic_id
            )
            return

        await safe_forward(msg, topic_id)

        dedup_cfg = DEDUP_TOPIC_RULES.get(topic_id)
        if dedup_cfg and dedup_cfg.get("dedup_include_edits"):
            fp = _make_fingerprint(msg)
            DEDUP_CACHE[(topic_id, fp)] = time.time()
            logger.debug(
                "DEDUP record_from_edit topic=%s msg_id=%s",
                topic_id,
                msg.id
            )

    except Exception as e:
        logger.exception("Edit handling failed: %s", e)
