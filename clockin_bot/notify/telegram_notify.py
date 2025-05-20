import requests
from clockin_bot.config.config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID
from clockin_bot.logger.logger import get_logger
from clockin_bot.logger.decorators import log_call

log = get_logger("telegram")

@log_call
def send_telegram_message(message: str):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
    }

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        log.info("成功發送 Telegram 訊息")
    except Exception as e:
        log.error(f"發送 Telegram 訊息失敗: {e}")

