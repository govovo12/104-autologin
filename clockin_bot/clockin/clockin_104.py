import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from tools.env_loader import *
from datetime import datetime
from playwright.sync_api import sync_playwright
from clockin_bot.notify.telegram_notify import send_telegram_message
from clockin_bot.logger.logger import get_logger
from clockin_bot.logger.decorators import log_call

log = get_logger("clockin")

BASE_DIR = Path(__file__).resolve().parent.parent
STORAGE_STATE_PATH = BASE_DIR / "data" / "login_state.json"

@log_call
def write_log(message):
    log_dir = BASE_DIR / "logs"
    log_dir.mkdir(exist_ok=True)
    log_path = log_dir / f"clockin_{datetime.now().date()}.log"
    with open(log_path, "a", encoding="utf-8") as log_file:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_file.write(f"[{timestamp}] {message}\n")

@log_call
def clockin_104():
    log.info("開始執行104打卡流程...")

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(storage_state=str(STORAGE_STATE_PATH))
            page = context.new_page()

            log.info("打卡頁面導向中...")
            page.goto("https://pro.104.com.tw/psc2?m=b,m,b,b")
            page.wait_for_timeout(5000)

            max_attempts = 3
            for attempt in range(1, max_attempts + 1):
                log.info(f"嘗試第 {attempt} 次打卡...")

                try:
                    with page.expect_response("**/api/f0400/newClockin", timeout=10000) as response_info:
                        page.evaluate("""
                            fetch("https://pro.104.com.tw/psc2/api/f0400/newClockin", {
                                method: "POST",
                                headers: {
                                    "Content-Type": "application/json"
                                }
                            })
                        """)
                        log.info("已發出打卡請求，等待回應...")

                    response = response_info.value
                    json_data = response.json()

                    if json_data.get("code") == 200 and json_data.get("message") == "OK":
                        att_id = json_data.get("data", {}).get("overAttCardDataId")
                        if att_id:
                            msg = f"打卡成功！(ID: {att_id})"
                            log.info(msg)
                            send_telegram_message(f"✅ [104] {msg}")
                            write_log(msg)

                            log.info("打卡成功後等待5秒...")
                            page.wait_for_timeout(5000)
                            break
                        else:
                            err = "API回傳成功，但未取得打卡ID"
                            log.warning(err)
                            send_telegram_message(err)
                            write_log(err)
                    else:
                        err = f"API回傳異常：{json_data}"
                        log.warning(err)
                        send_telegram_message("⚠️ 104打卡API異常")
                        write_log(err)

                except Exception as e:
                    err = f"打卡時發生例外錯誤：{e}"
                    log.error(err)
                    send_telegram_message("❌ 104打卡API請求失敗")
                    write_log(err)

            else:
                send_telegram_message("❌ 104打卡三次嘗試均失敗")
                write_log("104打卡三次嘗試均失敗")

            context.close()
            browser.close()
            return True

    except Exception as e:
        log.error(f"打卡流程發生錯誤：{e}")
        send_telegram_message(f"❌ 104打卡流程發生錯誤：{e}")
        write_log(f"打卡流程發生錯誤：{e}")
        return False

if __name__ == "__main__":
    clockin_104()

















