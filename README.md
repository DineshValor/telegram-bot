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
