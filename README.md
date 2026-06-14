# kkclip-formatter

Telegram bot built with aiogram: takes Instagram Reels links and returns
a link in kkclip.com format.

Example:

```
https://www.instagram.com/reel/DWZB5BfgO77/?igsh=MTVxMGZkMm50cjU4Nw==
```

->

```
https://www.kkclip.com/reel/DWZB5BfgO77/
```

## Running

1. Install dependencies:

   ```bash
   uv sync
   ```

2. Copy `.env.example` to `.env` and set your bot token:

   ```bash
   cp .env.example .env
   ```

3. Run:

   ```bash
   uv run python bot.py
   ```

## Running on a VPS (systemd)

Create `/etc/systemd/system/kkclip-bot.service`:

```ini
[Unit]
Description=kkclip formatter bot
After=network.target

[Service]
Type=simple
User=youruser
WorkingDirectory=/home/youruser/kkclip_formatter
EnvironmentFile=/home/youruser/kkclip_formatter/.env
ExecStart=/home/youruser/.local/bin/uv run python bot.py
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

Then:

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now kkclip-bot
```

Logs: `journalctl -u kkclip-bot -f`.
