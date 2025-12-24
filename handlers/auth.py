from telethon import events
from core.client import client
from utils.auth import is_admin, is_authorized, add_user

@client.on(events.NewMessage(pattern="/login"))
async def login_handler(event):
    user_id = event.sender_id

    if is_authorized(user_id):
        await event.reply("✅ You are already authorized.")
        return

    await event.reply(
        "📝 Login request received.\n"
        "Please wait for admin approval."
    )

@client.on(events.NewMessage(pattern="/approve"))
async def approve_handler(event):
    if not event.is_reply:
        return

    admin_id = event.sender_id
    if not is_admin(admin_id):
        await event.reply("❌ You are not an admin.")
        return

    reply_msg = await event.get_reply_message()
    user = await reply_msg.get_sender()

    add_user(user.id)

    await event.reply("✅ User approved successfully.")
