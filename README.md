## Telegram Bot (based on Telethon)

### Setup on Local Server - (CMD/Termux/Linux)
```
```

### Setup on Cloud Server - (Oracle/AWS using Console)
1️⃣ Clone repo
```
cd /opt
sudo git clone https://github.com/DineshValor/telegram-bot.git
```
2️⃣ Environment, dependencies & configure variables
```
cd telegram-bot
pip3 install -r requirements.txt
nano .env
```
3️⃣ Start bot
```
python3 bot.py
```
4️⃣ Manually update
```
sudo systemctl start telegram-bot-update.service
```

#### Run 24×7 (optional)

1️⃣ Copy systemd files
```
cd /opt/telegram-bot
sudo cp systemd/*.service systemd/*.timer /etc/systemd/system/
```

2️⃣ Enable & start services
```
sudo systemctl daemon-reload
sudo systemctl enable telegram-bot
sudo systemctl start telegram-bot

sudo systemctl enable telegram-bot-update.timer
sudo systemctl start telegram-bot-update.timer
```

### FAQ
#### Q. Fix ownership (IMPORTANT)
By default, cloning with sudo makes files owned by root.
If you plan to:
run bot as root → OK
run bot as a normal user (recommended later) → fix ownership
Example (recommended):
```
sudo chown -R ubuntu:ubuntu /opt/telegram-bot
```
(Replace ubuntu with your actual user.)

#### Q.
