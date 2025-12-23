## Telegram Telethon Bot (systemd)

### Setup (Oracle / Ubuntu / Termux / CMD)

```bash
git clone https://github.com/DineshValor/telegram-bot.git
cd telegram-bot
cp .env.example .env
nano .env
pip3 install -r requirements.txt
python3 bot.py
```
Install systemd
```

```
Logs
```
journalctl -u telegram-bot -f
```
---

# 🟡 ORACLE VM — ONE-TIME STEPS ONLY

After GitHub forked work is done 👇

```bash
sudo apt update && sudo apt install -y python3 python3-pip git
git clone https://github.com/DineshValor/telegram-bot.git
cd telegram-bot

pip3 install -r requirements.txt
cp .env.example .env
nano .env
python3 bot.py
```
From now on:
Push to GitHub → Oracle auto-updates
No SSH needed unless debugging
