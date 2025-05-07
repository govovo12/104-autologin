import time
import datetime
from pathlib import Path
from playwright.sync_api import sync_playwright
from scripts.telegram_notify import send_telegram_message

# === 設定旗標路徑 ===
BASE_DIR = Path(__file__).resolve().parent.parent
STORAGE_STATE_PATH = BASE_DIR / "data" / "login_state.json"

# --- 判斷是否打卡成功（比對新出現元素）
def is_clockin_success(page, old_elements):
    try:
        current_elements = set(page.locator("._2_body").all_inner_texts())
        new_elements = current_elements - old_elements  # 比對新增元素
        print("🆕 新出現的元素內容：", new_elements)
        return any("打卡成功" in text for text in new_elements)
    except Exception as e:
        print(f"❌ 比對打卡成功時發生錯誤：{e}")
        return False

# --- 主打卡流程 ---
def clockin_104():
    today = datetime.datetime.today().weekday()

    with sync_playwright() as p:
        browser = None
        context = None
        page = None
        success = False

        try:
            browser = p.chromium.launch(headless=False)
            context = browser.new_context(storage_state=str(STORAGE_STATE_PATH))
            page = context.new_page()

            print("🌐 開啟私人秘書打卡頁...")
            page.goto("https://pro.104.com.tw/psc2?m=b&m=b,b,b")
            page.wait_for_load_state("networkidle")
            page.wait_for_timeout(5000)

            print("🔍 打卡頁面載入完成，開始嘗試打卡...")

            for attempt in range(3):
                print(f"🔁 嘗試第 {attempt + 1} 次打卡...")

                try:
                    # 打卡前先抓現有的._2_body文字
                    old_elements = set(page.locator("._2_body").all_inner_texts())

                    button = page.locator(":text('打卡')").nth(5)
                    button.click()
                    print("🖱️ 打卡按鈕點擊完成，開始等待新提示...")

                    found_success = False

                    for wait_time in range(10):  # 最多等10秒，每秒比對一次
                        if is_clockin_success(page, old_elements):
                            found_success = True
                            break
                        time.sleep(1)

                    if found_success:
                        print("🎉 打卡成功！")
                        send_telegram_message("🎉 104 打卡成功！（已自動完成）")
                        success = True
                        break
                    else:
                        print("⚠️ 10秒內沒有新的打卡成功提示，準備下一次嘗試...")

                except Exception as e:
                    print(f"❌ 第 {attempt + 1} 次打卡出錯：{e}")

            if not success:
                print("🆘 三次打卡都失敗")
                send_telegram_message("❗️104 打卡失敗（重試三次仍未成功）")

            page.screenshot(path=str(BASE_DIR / "clockin_result.png"))

        except Exception as e:
            print(f"❗ 打卡主流程異常：{e}")

        finally:
            if page:
                page.close()
            if context:
                context.close()
            if browser:
                browser.close()

    return success

if __name__ == "__main__":
    clockin_104()






