"""Send alerts to Telegram and/or Discord (stdlib only). Config via env vars."""
import json
import os
import urllib.request


def _post_json(url, payload, timeout=15):
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.status


def send_telegram(text):
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")
    if not (token and chat_id):
        return False
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    try:
        _post_json(url, {"chat_id": chat_id, "text": text,
                         "parse_mode": "Markdown", "disable_web_page_preview": True})
        return True
    except Exception as e:
        print(f"[telegram] error: {e}")
        return False


def send_discord(text):
    webhook = os.environ.get("DISCORD_WEBHOOK_URL")
    if not webhook:
        return False
    try:
        _post_json(webhook, {"content": text[:1900]})
        return True
    except Exception as e:
        print(f"[discord] error: {e}")
        return False


def notify(text):
    """Send to all configured channels. Returns list of channels reached."""
    reached = []
    if send_telegram(text):
        reached.append("telegram")
    if send_discord(text):
        reached.append("discord")
    return reached


def configured():
    ch = []
    if os.environ.get("TELEGRAM_BOT_TOKEN") and os.environ.get("TELEGRAM_CHAT_ID"):
        ch.append("telegram")
    if os.environ.get("DISCORD_WEBHOOK_URL"):
        ch.append("discord")
    return ch
