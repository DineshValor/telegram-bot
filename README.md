## Telegram Bot (based on Telethon)

#### 🧱 1. Project Structure

✔ Clear separation of concerns

✔ No circular imports

✔ Easy to reason about
```
telegram-bot/
├── bot.py
├── requirements.txt
├── README.md
├── .gitignore
├── .*.session              # ❌ not committed (server only)
├── .env                    # ❌ not committed (server only)
│
├── config/
│   ├── __init__.py
│   ├── env.py
│   ├── forwarding.py
│   └── moderation.py
│
├── core/
│   ├── __init__.py
│   ├── client.py
│   └── startup.py
│
├── handlers/
│   ├── __init__.py
│   ├── forward.py
│   └── moderation.py
│
├── utils/
│   ├── __init__.py
│   ├── logger.py
│   └── messages.py
│
├── systemd/
│   ├── telegram-bot.service
│   ├── telegram-bot-update.service
│   ├── telegram-bot-update.timer
│   └── update.sh
│
└── venv/                   # ❌ not committed (server only)
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

1️⃣ SSH into Oracle server (or your preferred one)
```
ssh <PRIVATE_KEY> ubuntu@<SERVER_IP>
```

2️⃣ Clone Your GitHub Repository

If repo is not cloned
```
cd /home/ubuntu
git clone https://github.com/DineshValor/telegram-bot.git
```
If already cloned
```
cd /home/ubuntu/telegram-bot
git pull origin master
```

3️⃣ Create Python virtual environment
```
cd /home/ubuntu/telegram-bot
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
deactivate
```

4️⃣ Configure variables
```
nano /home/ubuntu/telegram-bot/.env
```

5️⃣ Make update script executable
```
chmod +x /home/ubuntu/telegram-bot/systemd/update.sh
```
Verify:
```
ls -l /home/ubuntu/telegram-bot/systemd/update.sh
```
You should see -rwx.

5️⃣ Start bot
```
cd /home/ubuntu/telegram-bot
source venv/bin/activate
python3 bot.py
```

#### Run 24×7 (Auto update + restart)

1️⃣ Stop bot
```
CTRL+C (Key Press)
```

2️⃣ Install systemd service files

Systemd cannot read files from your repo directly. We must copy them.
```
sudo cp /home/ubuntu/telegram-bot/systemd/telegram-bot.service /etc/systemd/system/
sudo cp /home/ubuntu/telegram-bot/systemd/telegram-bot-update.service /etc/systemd/system/
sudo cp /home/ubuntu/telegram-bot/systemd/telegram-bot-update.timer /etc/systemd/system/
```

3️⃣ Reload systemd
```
sudo systemctl daemon-reexec
sudo systemctl daemon-reload
```

4️⃣ Enable & start the bot
```
sudo systemctl enable telegram-bot
sudo systemctl start telegram-bot
```
Check status:
```
systemctl status telegram-bot
```
You should see:
```
Active: active (running)
```

5️⃣ Enable & start update timer
```
sudo systemctl enable telegram-bot-update.timer
sudo systemctl start telegram-bot-update.timer
```
Verify timer:
```
systemctl list-timers | grep telegram-bot
```
You should see next run time.

6️⃣ Verify logs (VERY IMPORTANT)

Bot logs:
```
journalctl -u telegram-bot -f
```
Update logs:
```
journalctl -u telegram-bot-update
```

7️⃣ Manual update test (optional but recommended)

Run update service manually:
```
sudo systemctl start telegram-bot-update.service
```
Expected behavior:
• If no new commit → “No updates found”
• If new commit → pull → restart bot

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

#### Q. Make update.sh executable
```
chmod +x /home/ubuntu/telegram-bot/systemd/update.sh
```

#### Q. Reload systemd
```
sudo systemctl daemon-reload
```

#### Q. If bot doesn’t start
journalctl -u telegram-bot --no-pager
