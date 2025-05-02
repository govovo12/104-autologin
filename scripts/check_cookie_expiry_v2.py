import json
import time
from datetime import datetime
from pathlib import Path

# === Cookie 狀態檢查腳本 ===
from telegram_notify import send_telegram_message

BASE_DIR = Path(__file__).resolve().parent.parent
COOKIE_PATH = BASE_DIR / "data" / "login_state.json"

IMPORTANT_COOKIES = [
    "ory_hydra_session",
    "laravel_session",
    "connect.sid",
    "hrm.connect.sid",
]

THRESHOLD_DAYS = 5  # 幾天內過期會觸發警告

def load_cookie_expiry():
    try:
        with open(COOKIE_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("cookies", [])
    except Exception as e:
        print(f"讀取 cookie 檔案失敗: {e}")
        send_telegram_message("⚠️ 無法讀取 login_state.json，請確認是否遺失！")
        return []

def check_cookie_expiry():
    cookies = load_cookie_expiry()
    if not cookies:
        send_telegram_message("⚠️ 找不到任何重要的 Cookie，請手動確認 104 登入狀態！")
        return

    now_ts = time.time()
    report_lines = ["[{}] ⚠️ Cookie狀態檢查".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))]
    sent_warning = False

    for cookie in cookies:
        if cookie.get("name") not in IMPORTANT_COOKIES:
            continue

        expiry = cookie.get("expires")
        if expiry is None or expiry == -1:
            continue

        remaining_days = int((expiry - now_ts) / 86400)
        status = "✅ Cookie狀態正常"

        if remaining_days <= 0:
            status = "❗ 已過期"
            sent_warning = True
        elif remaining_days <= THRESHOLD_DAYS:
            status = "注意：Cookie即將過期！"
            sent_warning = True

        report_lines.append("- Cookie名稱: {}".format(cookie["name"]))
        report_lines.append("- 預計到期日: {}".format(
            datetime.fromtimestamp(expiry).strftime("%Y-%m-%d")))
        report_lines.append("- 剩餘天數: {} 天".format(max(0, remaining_days)))
        report_lines.append("- 狀態: {}".format(status))

    if sent_warning:
        send_telegram_message("\n".join(report_lines))
    else:
        print("✅ 所有 Cookie 狀態正常，未送出 TG")

if __name__ == "__main__":
    check_cookie_expiry()

