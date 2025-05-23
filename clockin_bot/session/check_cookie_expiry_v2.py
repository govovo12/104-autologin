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

            cookies = cookie_data.get("cookies", [])
            valid_candidates = [
                c for c in cookies 
                if isinstance(c.get("expires"), (int, float)) and c["expires"] > 0
            ]

            if not valid_candidates:
                msg = "找不到任何具有效期限的 cookie，無法判斷剩餘天數"
                log.error(msg)
                send_telegram_message(msg)
                return False

            # 挑出過期時間最遠的那筆 cookie 作為參考
            best_cookie = max(valid_candidates, key=lambda c: c["expires"])
            cookie_name = best_cookie.get("name")
            expire_time = datetime.fromtimestamp(best_cookie["expires"])
            now = datetime.now()
            delta = expire_time - now
            delta_days = delta.days

            log.info(f"{cookie_name} 過期時間：{expire_time.strftime('%Y-%m-%d %H:%M:%S')}（剩餘 {delta_days} 天）")

            if delta.total_seconds() < 0:
                msg = f"❌ {cookie_name} 已過期，請重新登入"
                log.error(msg)
                send_telegram_message(msg)
                return False
            elif delta < timedelta(days=7):
                msg = f"⚠ {cookie_name} 快過期（剩 {delta_days} 天），請儘速重新登入"
                log.warning(msg)
                send_telegram_message(msg)
            else:
                msg = f"✅ {cookie_name} 尚未過期（剩餘 {delta_days} 天）"
                log.info(msg)
                send_telegram_message(msg)

            return True

    except Exception as e:
        msg = f"檢查 cookie 時發生錯誤：{e}"
        log.error(msg)
        send_telegram_message(msg)
        return False

__task_info__ = {
    "name": "check_cookie_expiry_v2",
    "desc": "分析 login_state.json 內最晚過期 cookie 的剩餘天數，並推播通知",
    "entry": check_cookie_expiry,
}

