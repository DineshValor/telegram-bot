from telethon import TelegramClient, events
from telethon.tl.types import MessageMediaPhoto, MessageMediaDocument

api_id = 22996249
api_hash = "e982daed463e4c9826c6c9ba828c2c37"

TARGET_GROUP = -1002303286535 # Ingress India 🇮🇳

CHANNEL_TOPIC_MAP = {
    -1001268572490: 1, # Dinesh Valor Channel -> Ingress India / XFaction Chat
    -1003341948290: 1, # Ingress India Test -> Ingress India / XFaction Chat
    
    -1001305415858: 15, # IngressFS Notifications -> Ingress India / First Saturday
    
    -1001008795454: 11079, # Passcodes Ingress PRIME ✳️ -> Ingress India / Ingress Updates
    -1001170454563: 11079, # Ingress -> Ingress India / Ingress Updates
    -1001126789733: 11079, Ingress Passcodes -> -> Ingress India / Ingress Updates
    
    -1001075281753: 8201, # Mission Banners, Oh My! (Global XFAC [ENG]) -> Ingress India / Mission Banners
    -1001078001228: 8201, # [Global] #MissionProject -> Ingress India / Mission Banners
    -1001420065662: 8201, # 📣 Ingress Mission Addicts -> -> Ingress India / Mission Banners
    
    -1002105354149: 1, # Ingress World Wide Competition 2025 -> Ingress India / XFaction Chat
    -1001167466234: 1, # NotNiantic Updates -> Ingress India / XFaction Chat
    -1001077599821: 1, # Ingress Updates [ENG] -> Ingress India / XFaction Chat
    -1001064978090: 1, # RGNN Ticker -> Ingress India / XFaction Chat
    -1001402896020: 1, # News_Hackventscalendar -> Ingress India / XFaction Chat
    -1001851154018: 1, # Ingress.Plus -> Ingress India / XFaction Chat
    -1001003824281: 1, # Enlightened Today -> Ingress India / XFaction Chat
    -1001837191055: 1, # Ingress Auctions -> Ingress India / XFaction Chat
}

MEDIA_ONLY_CHANNELS = {
  -1003341948290, # Ingress India Test -> Ingress India / XFaction Chat
  -1001075281753, # Mission Banners, Oh My! (Global XFAC [ENG]) -> Ingress India / Mission Banners
  -1001078001228, # [Global] #MissionProject -> Ingress India / Mission Banners
  -1001420065662, # 📣 Ingress Mission Addicts -> -> Ingress India / Mission Banners
  }
ALLOWED_EXTENSIONS = {".jpeg", ".jpg", ".png", ".zip", ".rar"}

client = TelegramClient("user_session", api_id, api_hash)

@client.on(events.NewMessage)
async def handler(event):
    chat_id = event.chat_id

    if chat_id not in CHANNEL_TOPIC_MAP:
        return

    topic_id = CHANNEL_TOPIC_MAP[chat_id]
    msg = event.message
    media = msg.media

    # 📷 Allow photos
    if isinstance(media, MessageMediaPhoto):
        pass

    # 📦 Allow documents with specific extensions
    elif isinstance(media, MessageMediaDocument):
        filename = msg.file.name or ""
        ext = "." + filename.lower().split(".")[-1] if "." in filename else ""

        if ext not in ALLOWED_EXTENSIONS:
            print(f"⛔ Blocked file {filename}")
            return

    # 🚫 Block non-media in restricted channels
    else:
        if chat_id in MEDIA_ONLY_CHANNELS:
            print("⛔ Blocked non-media message")
            return

    await client.send_message(
        TARGET_GROUP,
        msg,
        reply_to=topic_id
    )

    print(f"✅ Forwarded from {chat_id}")

client.start()
print("🚀 ID-based forwarding working correctly")
client.run_until_disconnected()
