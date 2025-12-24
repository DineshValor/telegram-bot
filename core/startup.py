from core.client import client
from db.database import init_db

def start_bot():
    init_db()
    client.start()
    print("🚀 Bot started successfully")
    client.run_until_disconnected()
