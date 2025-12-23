import os
import asyncio
from dotenv import load_dotenv

from telethon import TelegramClient, events
from telethon.tl.types import MessageMediaPhoto, MessageMediaDocument

# =========================
# LOAD ENV
# =========================
load_dotenv()

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")

if not API_ID or not API_HASH:
    raise RuntimeError("❌ API_ID or API_HASH missing in .env")

# =========================
# TELETHON CLIENT
# =========================
SESSION_NAME = "user_session"
client = TelegramClient(SESSION_NAME, API_ID, API_HASH)

# =========================
# TARGET GROUP (FORUM)
# =========================
TARGET_GROUP = int(os.getenv("TARGET_GROUP", "-1002303286535"))

# =========================
# SOURCE → TARGET TOPIC MAP
# =========================
CHANNEL_TOPIC_MAP = {
    -1001268572490: 1, # Dinesh Valor Channel -> Ingress India / XFaction Chat
    -1003341948290: 1, # Ingress India Test -> Ingress India / XFaction Chat
    
    -1001305415858: 15, # IngressFS Notifications -> Ingress India / First Saturday
    
    -1001008795454: 11079, # Passcodes Ingress PRIME -> Ingress India / Ingress Updates
    -1001170454563: 11079, # Ingress -> Ingress India / Ingress Updates
    -1001126789733: 11079, # Ingress Passcodes -> -> Ingress India / Ingress Updates
    
    -1001075281753: 8201, # Mission Banners, Oh My! (Global XFAC [ENG]) -> Ingress India / Mission Banners
    -1001078001228: 8201, # [Global] #MissionProject -> Ingress India / Mission Banners
    -1001420065662: 8201, # Ingress Mission Addicts -> -> Ingress India / Mission Banners
    
    -1002105354149: 1, # Ingress World Wide Competition 2025 -> Ingress India / XFaction Chat
    -1001167466234: 1, # NotNiantic Updates -> Ingress India / XFaction Chat
    -1001077599821: 1, # Ingress Updates [ENG] -> Ingress India / XFaction Chat
    -1001064978090: 1, # RGNN Ticker -> Ingress India / XFaction Chat
    -1001402896020: 1, # News_Hackventscalendar -> Ingress India / XFaction Chat
    -1001851154018: 1, # Ingress.Plus -> Ingress India / XFaction Chat
    -1001003824281: 1, # Enlightened Today -> Ingress India / XFaction Chat
    -1001837191055: 1, # Ingress Auctions -> Ingress India / XFaction Chat
}

# =========================
# MEDIA-ONLY SOURCE CHANNELS
# =========================
MEDIA_ONLY_CHANNELS = {
    -1003341948290, # Ingress India Test -> Ingress India / XFaction Chat
    -1001075281753, # Mission Banners, Oh My! (Global XFAC [ENG]) -> Ingress India / Mission Banners
    -1001078001228, # [Global] #MissionProject -> Ingress India / Mission Banners
    -1001420065662, # Ingress Mission Addicts -> -> Ingress India / Mission Banners
}

ALLOWED_EXTENSIONS = {".jpeg", ".jpg", ".png", ".zip", ".rar"}

# ============================================================
# 1️⃣ FORWARDING HANDLER
# ============================================================
@client.on(events.NewMessage)
async def forward_handler(event):
    chat_id = event.chat_id

    if chat_id not in CHANNEL_TOPIC_MAP:
        return

    topic_id = CHANNEL_TOPIC_MAP[chat_id]
    msg = event.message
    media = msg.media

    if chat_id in MEDIA_ONLY_CHANNELS:
        if not media:
            return

        if isinstance(media, MessageMediaPhoto):
            return

        if isinstance(media, MessageMediaDocument):
            filename = msg.file.name or ""
            ext = "." + filename.lower().split(".")[-1] if "." in filename else ""
            if ext not in ALLOWED_EXTENSIONS:
                return
        else:
            return

    await client.send_message(
        TARGET_GROUP,
        msg,
        reply_to=topic_id
    )

    print(f"✅ Forwarded from {chat_id}")

# ============================================================
# 2️⃣ TOPIC RULES
# ============================================================
TOPIC_RULES = {
    10: {        # 🏆 Bragging Rights
        "text": False,
        "photo": True,
        "video": True,
        "doc_ext": {".jpg", ".jpeg", ".png", ".mp4"},
    },
    8201: {      # 🎭 Mission Banners
        "text": False,
        "photo": True,
        "video": False,
        "doc_ext": {".jpg", ".jpeg", ".png", ".zip", ".rar"},
    },
}

# ============================================================
# 3️⃣ MODERATION REPLY HELPER
# ============================================================
async def send_reason(topic_id, reason, offender, ttl=30):
    mention = "Unknown user"

    try:
        user = await offender.get_sender()
        if user:
            mention = f"[{user.first_name}](tg://user?id={user.id})"
    except Exception:
        pass

    reply = await client.send_message(
        TARGET_GROUP,
        (
            "⚠️ **Message removed**\n"
            f"👤 User: {mention}\n"
            f"📌 Reason: {reason}"
        ),
        reply_to=topic_id,
        parse_mode="md"
    )

    await asyncio.sleep(ttl)
    await reply.delete()

# ============================================================
# 4️⃣ DELETE HANDLER (TARGET GROUP)
# ============================================================
@client.on(events.NewMessage(chats=TARGET_GROUP))
async def delete_handler(event):
    msg = event.message

    if not msg or not msg.reply_to:
        return

    # Ignore bot's own moderation messages
    me = await client.get_me()
    if msg.from_id and msg.from_id.user_id == me.id:
        return

    topic_id = msg.reply_to.reply_to_msg_id
    rules = TOPIC_RULES.get(topic_id)

    if not rules:
        return

    # 📝 TEXT
    if msg.text and not msg.media:
        if not rules["text"]:
            await msg.delete()
            await send_reason(
                topic_id,
                (
                    "Text messages are not allowed in this topic.\n\n"
                    "👉 Kindly switch to "
                    "[#XFaction-Chat](https://t.me/IngressIN/1) "
                    "for chat & discussion."
                ),
                msg
            )
        return

    media = msg.media

    # 🖼 PHOTO
    if isinstance(media, MessageMediaPhoto):
        if not rules["photo"]:
            await msg.delete()
            await send_reason(topic_id, "Photos are not allowed in this topic.", msg)
        return

    # 🎥 VIDEO
    if msg.video:
        if not rules["video"]:
            await msg.delete()
            await send_reason(topic_id, "Videos are not allowed in this topic.", msg)
        return

    # 📦 DOCUMENT
    if isinstance(media, MessageMediaDocument) and not msg.video:
        filename = msg.file.name or "unknown file"
        ext = "." + filename.lower().split(".")[-1] if "." in filename else ""

        if ext not in rules["doc_ext"]:
            allowed = ", ".join(sorted(rules["doc_ext"]))
            await msg.delete()
            await send_reason(
                topic_id,
                f"File type `{ext}` is not allowed here.\nAllowed: {allowed}",
                msg
            )
        return

# =========================
# START CLIENT
# =========================
client.start()
print("🚀 Forwarding + topic moderation active")
client.run_until_disconnected()
