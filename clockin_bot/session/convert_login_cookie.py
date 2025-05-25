import json
from pathlib import Path
from clockin_bot.logger.logger import get_logger
from clockin_bot.logger.decorators import log_call
from clockin_bot.notify.telegram_notify import send_telegram_message
from clockin_bot.clockin.base.result import TaskResult, ResultCode

log = get_logger("cookie_converter")

BASE_DIR = Path(__file__).resolve().parent.parent
LOGIN_STATE_FILE = BASE_DIR / "data" / "login_state.json"
COOKIE_HEADER_FILE = BASE_DIR / "data" / "cookie_header.json"

@log_call
def convert_login_state_to_cookie_header(domain_filter="pro.104.com.tw"):
    if not LOGIN_STATE_FILE.exists():
        msg = f"❌ 找不到 login_state.json：{LOGIN_STATE_FILE}"
        log.error(msg)
        send_telegram_message(msg)
        return TaskResult(code=ResultCode.COOKIE_FILE_NOT_FOUND, message=msg)

    try:
        with open(LOGIN_STATE_FILE, encoding="utf-8") as f:
            data = json.load(f)

        cookies = data.get("cookies", [])
        if not cookies:
            msg = "⚠ login_state.json 中沒有 cookies 資料"
            log.warning(msg)
            send_telegram_message(msg)
            return TaskResult(code=ResultCode.COOKIE_PARSE_ERROR, message=msg)

        filtered = [
            f"{c['name']}={c['value']}"
            for c in cookies
            if domain_filter in c.get("domain", "")
        ]

        if not filtered:
            msg = f"⚠ 找不到符合 {domain_filter} 的 cookie"
            log.warning(msg)
            send_telegram_message(msg)
            return TaskResult(code=ResultCode.COOKIE_PARSE_ERROR, message=msg)

        header_data = {
            "cookie": "; ".join(filtered),
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
        }

        with open(COOKIE_HEADER_FILE, "w", encoding="utf-8") as f:
            json.dump(header_data, f, indent=2, ensure_ascii=False)

        msg = f"✅ cookie_header.json 已成功產生，共 {len(filtered)} 筆 cookie"
        log.info(msg)
        send_telegram_message(msg)
        return TaskResult(code=ResultCode.SUCCESS, message=msg)

    except Exception as e:
        msg = f"❌ 轉換過程發生錯誤：{e}"
        log.exception(msg)
        send_telegram_message(msg)
        return TaskResult(code=ResultCode.COOKIE_PARSE_ERROR, message=msg)


__task_info__ = {
    "name": "convert_cookie",
    "desc": "轉換 login_state.json 為 cookie_header.json（只抓 pro.104.com.tw）",
    "entry": convert_login_state_to_cookie_header,
}
