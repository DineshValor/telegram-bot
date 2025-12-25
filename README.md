## Telegram Bot (based on Telethon)

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
```
3️⃣ Install dependencies & configure variables
```
pip install -r requirements.txt
nano .env
```
4️⃣ Start bot
```
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

3️⃣ Enable & start services
```
sudo systemctl daemon-reload
sudo systemctl enable telegram-bot
sudo systemctl start telegram-bot

sudo systemctl enable telegram-bot-update.timer
sudo systemctl start telegram-bot-update.timer
```

### FAQ
#### Q. Fix Ownership (IMPORTANT)
By default, cloning with sudo makes files owned by root.

If you plan to:

run bot as root → OK

run bot as a normal user (recommended later) → fix ownership

Example (recommended):
```
sudo chown -R ubuntu:ubuntu /opt/telegram-bot
```
(Replace ubuntu with your actual user.)

#### Q. Check Timer
Even without waiting:
```
systemctl status telegram-bot-update.timer
systemctl list-timers | grep telegram-bot
```
This only confirms scheduling, not logic.

#### Q. Manually Update
```
sudo systemctl start telegram-bot-update.service
```
#### Q. Check Bot Service
```
sudo systemctl status telegram-bot
journalctl -u telegram-bot -f
```

#### Q. Fix Manual Update Error
```
sudo git config --system --add safe.directory /opt/telegram-bot
```

#### Q. Fix root shell permission
```
sudo chown -R ubuntu:ubuntu /opt
```

#### Q. Update Systemd files
```
sudo systemctl daemon-reload

sudo systemctl enable telegram-bot.service
sudo systemctl restart telegram-bot.service

sudo systemctl enable telegram-bot-update.timer
sudo systemctl restart telegram-bot-update.timer
```

#### Q. Recover Failed State Systemd
```
sudo systemctl reset-failed telegram-bot
sudo systemctl restart telegram-bot
```
