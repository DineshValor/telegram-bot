## Telegram Telethon Bot (systemd)

### Setup (Oracle / Ubuntu)

```bash
git clone https://github.com/DineshValor/telegram-bot.git
cd telegram-bot
cp .env.example .env
nano .env
pip3 install -r requirements.txt
```
---

# 🟡 ORACLE VM — ONE-TIME STEPS ONLY

After GitHub work is done 👇

```bash
sudo apt update && sudo apt install -y python3 python3-pip git
git clone https://github.com/DineshValor/telegram-bot.git
cd telegram-bot

pip3 install -r requirements.txt
cp .env.example .env
nano .env

sudo cp systemd/*.service systemd/*.timer /etc/systemd/system/
sudo systemctl daemon-reload

sudo systemctl enable telegram-bot
sudo systemctl start telegram-bot
sudo systemctl enable telegram-bot-update.timer
sudo systemctl start telegram-bot-update.timer
```
