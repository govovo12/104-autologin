import time
import datetime
from pathlib import Path
from playwright.sync_api import sync_playwright
from scripts.telegram_notify import send_telegram_message  # ✅ 因為放在 scripts 目錄下
# === 設定旗標路徑 ===
BASE_DIR = Path(__file__).resolve().parent.parent
STORAGE_STATE_PATH = BASE_DIR / "data" / "login_state.json"

def is_clockin_success(page):
    try:
        elements = page.locator("._2_body").all_inner_texts()
        print("🧪 判斷提示框內容：", elements)
        return any("打卡成功" in text for text in elements)
    except Exception as e:
        print(f"❌ 讀取打卡提示時發生錯誤：{e}")
        return False

def clockin_104():
    today = datetime.datetime.today().weekday()
# if today > 4:
#     print("🚫 今天是週六或週日，不執行打卡！")
#     return

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(storage_state=str(STORAGE_STATE_PATH))
        page = context.new_page()

        print("🌐 開啟私人秘書打卡頁...")
        page.goto("https://pro.104.com.tw/psc2?m=b&m=b,b,b")
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(5000)

        if is_clockin_success(page):
            print("✅ 今天已經打過卡，跳過")
            send_telegram_message("✅ 今天已經打過卡（略過打卡）")
        else:
            print("🕒 尚未打卡，準備開始嘗試最多3次")
            success = False

            for attempt in range(3):
                print(f"🔁 嘗試第 {attempt + 1} 次打卡...")
                try:
                    page.locator(":text('打卡')").nth(5).click()
                    time.sleep(2.5)
                    if is_clockin_success(page):
                        print("🎉 打卡成功！")
                        send_telegram_message("🎉 104 打卡成功！（已自動完成）")
                        success = True
                        break
                    else:
                        print("⚠️ 沒看到成功提示，繼續重試")
                except Exception as e:
                    print(f"❌ 第{attempt + 1}次打卡點擊失敗：{e}")

            if not success:
                print("🆘 三次打卡都失敗")
                send_telegram_message("❗️104 打卡失敗（重試三次仍未成功）")

        page.screenshot(path=str(BASE_DIR / "clockin_result.png"))
        browser.close()

if __name__ == "__main__":
    clockin_104()



