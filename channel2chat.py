from telethon import TelegramClient, events

api_id = 24474379
api_hash = "e994452a74a2e0a053827d0f63e4c3b0"

TARGET_GROUP = -1002303286535  # forum group ID

CHANNEL_TOPIC_MAP = {
    "NotNianticUpdates": 11079, # Ingress Updates topic ID
    "IngressFSNews": 15,        # First Saturday topic ID
    "NianticOfficial": 11079,   # Ingress Updates topic ID
    "IUENG": 11079,   # Ingress Updates topic ID
    "IWWC2025": 1,  # Ingress Updates topic ID
    "HackventscalendarNews": 1, # Ingress Updates topic ID
    "IngressMissionAddicts": 8201, # Mission Banners topic ID
    "dineshvalorchannel": 1, # Test Updates
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
