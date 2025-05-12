import sys
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from pathlib import Path
from datetime import datetime
from playwright.sync_api import sync_playwright
from scripts.telegram_notify import send_telegram_message

BASE_DIR = Path(__file__).resolve().parent.parent
STORAGE_STATE_PATH = BASE_DIR / "data" / "login_state.json"

def write_log(message):
    log_dir = BASE_DIR / "logs"
    log_dir.mkdir(exist_ok=True)
    log_path = log_dir / f"clockin_{datetime.now().date()}.log"
    with open(log_path, "a", encoding="utf-8") as log_file:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_file.write(f"[{timestamp}] {message}\n")

def clockin_104():
    print("🚀 啟動正式打卡流程（104）...")

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            context = browser.new_context(storage_state=str(STORAGE_STATE_PATH))
            page = context.new_page()

            print("🌐 導向打卡頁面...")
            page.goto("https://pro.104.com.tw/psc2?m=b&m=b,b,b")
            page.wait_for_load_state("networkidle")
            page.wait_for_timeout(3000)  # 等待登入狀態與 session 生效

            max_attempts = 3
            for attempt in range(1, max_attempts + 1):
                print(f"🔁 第 {attempt} 次打卡嘗試...")

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
                        print("🛰️ 已發送打卡請求，等待回應...")

                    response = response_info.value
                    json_data = response.json()

                    if json_data.get("code") == 200 and json_data.get("message") == "OK":
                        att_id = json_data.get("data", {}).get("overAttCardDataId")
                        if att_id:
                            msg = f"✅ 打卡成功（ID: {att_id}）"
                            print(msg)
                            send_telegram_message("✅ [104] 打卡成功！")
                            write_log(msg)
                            break
                        else:
                            err = "⚠️ API 回傳成功但無打卡 ID"
                            print(err)
                            send_telegram_message(err)
                            write_log(err)
                    else:
                        err = f"⚠️ API 回應異常：{json_data}"
                        print(err)
                        send_telegram_message("⚠️ 打卡 API 回應異常")
                        write_log(err)

                except Exception as e:
                    err = f"❌ 打卡錯誤：{e}"
                    print(err)
                    send_telegram_message("❌ 打卡 API 發送或解析失敗")
                    write_log(err)

            else:
                send_telegram_message("❌ 所有打卡嘗試皆失敗")
                write_log("❌ 所有打卡嘗試皆失敗")

            context.close()
            browser.close()
            return True

    except Exception as e:
        print(f"⚠️ 發生錯誤：{e}")
        send_telegram_message(f"⚠️ 打卡腳本發生錯誤：{e}")
        write_log(f"⚠️ 發生錯誤：{e}")
        return False

if __name__ == "__main__":
    clockin_104()















