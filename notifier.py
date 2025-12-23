import os, sys, requests
from dotenv import load_dotenv

load_dotenv("config.env")

BOT = os.getenv("ALERT_BOT_TOKEN")
CHAT = os.getenv("ALERT_CHAT_ID")

def send(msg):
    if not BOT or not CHAT:
        return
    url = f"https://api.telegram.org/bot{BOT}/sendMessage"
    requests.post(url, data={"chat_id": CHAT, "text": msg})

if __name__ == "__main__":
    send(" ".join(sys.argv[1:]))
