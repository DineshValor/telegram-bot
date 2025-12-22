from telethon import TelegramClient, events

api_id = 22996249
api_hash = "e982daed463e4c9826c6c9ba828c2c37"

TARGET_GROUP = -1002303286535  # forum group ID

CHANNEL_TOPIC_MAP = {
    "NotNianticUpdates": 1, # XFaction Chat topic ID
    "IngressFSNews": 15,        # First Saturday topic ID
    "NianticOfficial": 11079,   # Ingress Updates topic ID
    "IUENG": 1,   # XFaction Chat topic ID
    "IWWC2025": 1,  # XFaction Chat topic ID
    "HackventscalendarNews": 1, # XFaction Chat topic ID
    "IngressMissionAddicts": 8201, # Mission Banners topic ID
    "IEToday": 1, # XFaction Chat topic ID
    "RGNNticker": 1, # XFaction Chat topic ID
    "PasscodesIngress": 11079, # Ingress Updates topic ID
    "IngressAuctions": 1, # XFaction Chat topic ID
    "dineshvalorchannel": 1, # Test Updates (XFaction Chat) topic ID
}

client = TelegramClient("user_session", api_id, api_hash)

@client.on(events.NewMessage(chats=list(CHANNEL_TOPIC_MAP.keys())))
async def handler(event):
    topic_id = CHANNEL_TOPIC_MAP.get(event.chat.username)

    await client.send_message(
    TARGET_GROUP,
    event.message,
    reply_to=topic_id
)

client.start()
print("✅ Forwarding to specific topics...")
client.run_until_disconnected()
