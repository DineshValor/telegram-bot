from core.client import client

def start_bot():
    client.start()
    print("🚀 Bot started successfully")
    client.run_until_disconnected()
