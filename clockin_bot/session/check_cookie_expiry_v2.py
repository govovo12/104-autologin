import json
from datetime import datetime, timedelta
from pathlib import Path
from clockin_bot.logger.logger import get_logger
from clockin_bot.logger.decorators import log_call
from clockin_bot.notify.telegram_notify import send_telegram_message

log = get_logger("cookie_checker")

BASE_DIR = Path(__file__).resolve().parent.parent
COOKIE_FILE = BASE_DIR / "data" / "login_state.json"

@log_call
def check_cookie_expiry():
    if not COOKIE_FILE.exists():
        msg = f"找不到 cookie 檔案：{COOKIE_FILE}"
        log.error(msg)
        send_telegram_message(msg)
        return False

    try:
        with open(COOKIE_FILE, "r", encoding="utf-8") as f:
            cookie_data = json.load(f)
            for cookie in cookie_data.get("cookies", []):
                if cookie.get("name") == "sid":
                    expires = cookie.get("expires")
                    if not expires:
                        msg = "sid 欄位沒有 expires，cookie 已過期"
                        log.error(msg)
                        send_telegram_message(msg)
                        return False

                    expire_time = datetime.fromtimestamp(expires)
                    now = datetime.now()
                    delta = expire_time - now
                    log.info(f"sid 過期時間：{expire_time.strftime('%Y-%m-%d %H:%M:%S')}（剩餘 {delta.days} 天）")

                    if delta < timedelta(days=7):
                        msg = f"sid 快過期（剩 {delta.days} 天），請儘速重新登入"
                        log.warning(msg)
                        send_telegram_message(msg)
                    else:
                        log.info("sid 尚未過期，無需重新登入")

                    return True

            msg = "cookie 資料中找不到 sid"
            log.error(msg)
            send_telegram_message(msg)
            return False

    except Exception as e:
        msg = f"檢查 cookie 時發生錯誤：{e}"
        log.error(msg)
        send_telegram_message(msg)
        return False

if __name__ == "__main__":
    check_cookie_expiry()
