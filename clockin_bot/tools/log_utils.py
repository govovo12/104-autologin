from clockin_bot.logger.logger import get_logger
from clockin_bot.notify.telegram_notify import send_telegram_message
from clockin_bot.tools.upload_log_to_pages import upload_log_only as upload_log
from clockin_bot.clockin.base.result import TaskResult, ResultCode

log = get_logger(__name__)

def report_and_notify(result: TaskResult) -> None:
    """
    根據 TaskResult 發送通知並寫入 log。
    若成功僅記錄訊息，若失敗則記錄錯誤並上傳 log。
    """
    if result.code == ResultCode.SUCCESS:
        log.info(result.message)
        send_telegram_message(f"✅ {result.message}")
    else:
        log.error(f"[{result.code.name}] {result.message}")
        send_telegram_message(f"❌ [{result.code.name}] {result.message}")
        upload_log()
