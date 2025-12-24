from core.client import client

import handlers.forward
import handlers.moderation

client.start()
print("🚀 Forwarding + moderation active")
client.run_until_disconnected()
