from datetime import datetime
import requests
from clockin_bot.config import config
from clockin_bot.clockin.base.result import TaskResult, ResultCode
from clockin_bot.logger.logger import get_logger
from clockin_bot.logger.decorators import log_call

log = get_logger("telegram")

# GitHub Pages 設定（未來若更動報告網址，改這裡即可）
REPORT_URL = "https://govovo12.github.io/104-autologin/latest_log_view.html"

@log_call
def send_telegram_message(message: str) -> TaskResult:
    # 使用 config 模組中的 TOKEN 與 CHAT_ID
    if not config.TELEGRAM_BOT_TOKEN or not config.TELEGRAM_CHAT_ID:
        msg = "未設定 Telegram BOT TOKEN 或 CHAT ID，略過推播"
        log.warning(msg)
        return TaskResult(code=ResultCode.NOTIFY_SKIP, message=msg)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    full_message = f"{message}\n📅 {timestamp}\n🔗 報告網址：{REPORT_URL}"

    url = f"https://api.telegram.org/bot{config.TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": config.TELEGRAM_CHAT_ID,
        "text": full_message
    }

    try:
        response = requests.post(url, json=payload, timeout=5)
        response.raise_for_status()
        log.info("成功發送 Telegram 訊息")
        return TaskResult(code=ResultCode.SUCCESS, message="已推播 Telegram")
    except Exception as e:
        err = f"發送 Telegram 訊息失敗: {e}"
        log.error(err)
        return TaskResult(code=ResultCode.NOTIFY_FAILED, message=err)

__task_info__ = {
    "name": "send_telegram_message",
    "desc": "透過 Telegram BOT 發送訊息通知，含報告網址與時間戳",
    "entry": send_telegram_message
}
