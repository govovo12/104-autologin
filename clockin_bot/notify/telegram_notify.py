from datetime import datetime
import os
import requests
from clockin_bot.config.config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

# GitHub Pages 設定（若未來想改路徑，改這個變數即可）
REPORT_URL = "https://govovo12.github.io/104-autologin/latest_log_view.html"

def send_telegram_message(message: str):
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("❌ 未設定 Telegram BOT TOKEN 或 CHAT ID，略過推播")
        return

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    full_message = (
        f"{message}\n"
        f"📅 {timestamp}\n"
        f"🔗 報告網址：{REPORT_URL}"
    )

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": full_message
    }

    try:
        response = requests.post(url, json=payload, timeout=5)
        response.raise_for_status()
        print("[INFO][telegram] 成功發送 Telegram 訊息")
    except Exception as e:
        print(f"[ERROR][telegram] 發送 Telegram 訊息失敗: {e}")
