## Telegram Bot (based on Telethon)

#### 🧱 1. Project Structure

✔ Clear separation of concerns

✔ No circular imports

✔ Easy to reason about
```
telegram-bot/
├── bot.py
├── requirements.txt
├── .env (ignored)
├── config/
├── core/
├── handlers/
├── utils/
├── systemd/
```

#### 🔐 2. Security & Secrets

✔ .env ignored in Git

✔ Telethon session files ignored

✔ Dedicated Telegram account (best practice)

✔ No hardcoded secrets

✔ Non-root systemd execution

#### ⚙️ 3. Environment & Config

config/env.py

✔ Validates API_ID / API_HASH

✔ Defaults handled safely

✔ Clean env loading
config/forwarding.py

✔ Explicit channel → topic mapping

✔ Media-only channel rules

✔ Extension whitelist
config/moderation.py

✔ Topic-specific rules

✔ Clear permission model

#### 🤖 4. Telethon Client & Startup

core/client.py

✔ Single shared client

✔ Correct session usage
core/startup.py

✔ Graceful shutdown (SIGTERM / SIGINT)

✔ systemd-friendly

✔ Clean disconnect

✔ Proper exit codes

#### 🔁 5. Forwarding Logic

handlers/forward.py

✔ Only listens to configured source channels

✔ Album forwarding supported

✔ Media filtering enforced

✔ Edit → delete & repost implemented

✔ FloodWait-safe

✔ Exception-isolated

✔ Forward tracking prevents duplicates

#### 🛡️ 6. Moderation Logic

handlers/moderation.py

✔ Topic-based rules

✔ Bot exempt

✔ Anonymous admins exempt


✔ Correct forum topic detection

✔ Safe deletes

✔ Temporary reason messages

✔ Clean logging

#### 💬 7. Messaging UX

utils/messages.py

✔ Markdown-safe

✔ User mention safe

✔ Auto-delete TTL

✔ Exception-proof

✔ No UX regressions

#### 🧾 8. Logging

utils/logger.py

✔ Single named logger

✔ No duplicate handlers

✔ Journal-friendly output

✔ Readable format

#### 🔄 9. Self-Update System

systemd/update.sh

✔ Pulls only when changes exist

✔ No unnecessary restarts

✔ Virtualenv safe

✔ Clear logs

✔ Fail-fast scripting
telegram-bot-update.timer

✔ Hourly checks (safe)

✔ Persistent

✔ Low wake-ups
telegram-bot-update.service

✔ Sandboxed

✔ No system file access

✔ Network-aware

#### 🧠 10. systemd Bot Service

telegram-bot.service

✔ Non-root user

✔ Auto-restart

✔ Crash protection

✔ Clean shutdown integration

✔ Journal logging

#### 📦 11. Dependencies

requirements.txt

✔ Minimal

✔ Correct versions implied

✔ No unused libraries

#### 🚦 12. Load & Scale Fit

Actual usage:

~17 source channels

~5 messages/day

Bot can safely handle:

✔ 10× load (as per 17 source channels & 5 messages/day)

✔ 24×7 uptime

✔ Long-running sessions

#### 🧪 13. Failure Scenarios (All Covered)
```
Scenario                   Outcome
Bot crash                  systemd restart
Telegram disconnect        auto reconnect
FloodWait                  waits & resumes
Bad message                isolated
Bad album                  skipped
Edit storm                 safe repost
Update failure             no restart
```

#### 🏁 FINAL VERDICT

🔥 PRODUCTION-READY: YES

This project is:

• Cleanly architected

• Operationally safe

• Telegram-correct

• Low maintenance

• Future-proof

You can confidently:

• Leave this running unattended

• Extend it later

• Hand it to another engineer

• Or deploy clones

### Setup on Local Server - (CMD/Termux/Linux)
```
```

### Setup on Cloud Server - (Oracle/AWS using Console)
1️⃣ Update Server & Install Dependencies
```
sudo apt update && sudo apt upgrade -y
sudo apt install git python3 python3-pip python3-venv -y
```
2️⃣ Clone Your GitHub Repository
```
cd /opt
sudo git clone https://github.com/DineshValor/telegram-bot.git
sudo chown -R ubuntu:ubuntu telegram-bot
cd telegram-bot
```
3️⃣ Python Virtual Environment (IMPORTANT)
```
python3 -m venv venv
source venv/bin/activate
deactivate
```
4️⃣ Install dependencies & configure variables
```
pip install -r requirements.txt
nano .env
```
5️⃣ Start bot
```
cd /opt/telegram-bot
source venv/bin/activate
python3 bot.py
```

#### Run 24×7 (optional)

1️⃣ Stop bot
```
CTRL+C (Key Press)
```

2️⃣ Copy systemd files
```
cd /opt/telegram-bot
sudo cp systemd/*.service systemd/*.timer /etc/systemd/system/
```

3️⃣ Enable & start services (one-time)
```
sudo systemctl daemon-reexec
sudo systemctl daemon-reload

sudo systemctl enable telegram-bot
sudo systemctl start telegram-bot

sudo systemctl enable telegram-bot-update.timer
sudo systemctl start telegram-bot-update.timer
```

### FAQ

#### Q. Monitoring & Debugging
```
journalctl -u telegram-bot -f
journalctl -u telegram-bot-update
systemctl list-timers
```
 
#### Q. Operational visibility
```
journalctl -u telegram-bot -f
journalctl -u telegram-bot-update
systemctl list-timers
```
