import requests
import json
from pathlib import Path
from datetime import datetime
from clockin_bot.logger.logger import get_logger
from clockin_bot.logger.decorators import log_call
from clockin_bot.notify.telegram_notify import send_telegram_message

BASE_DIR = Path(__file__).resolve().parent.parent
cookie_path = BASE_DIR / "data" / "cookie_header.json"
log = get_logger("clockin")

# 讀取 Cookie
with open(cookie_path, encoding="utf-8") as f:
    COOKIE_HEADER = json.load(f)["cookie"]

headers = {
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0",
    "cookie": COOKIE_HEADER
}

@log_call
def write_log(message):
    log_path = BASE_DIR / "logs" / f"clockin_{datetime.now().date()}.log"
    log_path.parent.mkdir(exist_ok=True)
    with open(log_path, "a", encoding="utf-8") as log_file:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_file.write(f"[{timestamp}] {message}\n")

@log_call
def clockin_104():
    log.info("開始執行 104 打卡流程（requests 版本）...")
    try:
        response = requests.post(
            "https://pro.104.com.tw/psc2/api/f0400/newClockin",
            headers=headers,
            timeout=10
        )

        log.info(f"回傳狀態：{response.status_code}")
        try:
            res_json = response.json()
            log.info(f"回傳內容：{json.dumps(res_json, ensure_ascii=False)}")
        except Exception as e:
            res_json = {}
            log.warning(f"無法解析 JSON：{e}")

        if response.status_code == 200 and res_json.get("code") == 200:
            att_id = res_json.get("data", {}).get("overAttCardDataId")
            if att_id:
                msg = f"打卡成功！(ID: {att_id})"
                log.info(msg)
                send_telegram_message(f"✅ [104] {msg}")
                write_log(msg)
                return True
            else:
                err = "API 回傳成功，但未取得打卡 ID"
        else:
            err = f"打卡失敗，狀態碼：{response.status_code}，內容：{res_json}"

    except Exception as e:
        err = f"打卡流程發生例外錯誤：{e}"

    log.error(err)
    send_telegram_message(f"❌ 104 打卡失敗：{err}")
    write_log(err)
    return False

__task_info__ = {
    "name": "clockin_104",
    "desc": "發送 requests API 進行 104 打卡，推播 Telegram 成功通知",
    "entry": clockin_104,
}
