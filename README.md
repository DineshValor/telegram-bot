## Telegram Bot (based on Telethon)

### Setup on Local Server - (CMD/Termux/Linux)
```
```

### Setup on Cloud Server - (Oracle/AWS using Console)
(Follow any tutorial on youtube "how to setup instance on cloud server")
```

```

#### Run 24×7
Step 1️⃣ Clone repo
```
cd /opt
sudo git clone https://github.com/DineshValor/telegram-bot.git
```
Step 2️⃣ Copy systemd files
```
sudo cp systemd/*.service systemd/*.timer /etc/systemd/system/
```
Step 3️⃣ Enable & start services
```
sudo systemctl daemon-reload
sudo systemctl enable telegram-bot
sudo systemctl start telegram-bot

sudo systemctl enable telegram-bot-update.timer
sudo systemctl start telegram-bot-update.timer
```
