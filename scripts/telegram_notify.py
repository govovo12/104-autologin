# telegram_notify.py
import requests
from datetime import datetime
from scripts.config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

def send_telegram_message(message):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # 取得現在時間
    full_message = f"[{now}] {message}"  # 把時間標籤加在最前面

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": full_message
    }
    try:
        response = requests.post(url, data=payload)
        response.raise_for_status()
        print("📬 成功發送Telegram訊息")
    except Exception as e:
        print(f"❌ 發送Telegram訊息失敗：{e}")
