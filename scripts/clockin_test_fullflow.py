from pathlib import Path
from playwright.sync_api import sync_playwright

BASE_DIR = Path(__file__).resolve().parent
STORAGE_STATE_PATH = BASE_DIR.parent / "data" / "login_state.json"

CLOCKIN_API_URL = "https://pro.104.com.tw/psc2/api/f0400/newClockin"

def clockin_test_fullflow():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(storage_state=str(STORAGE_STATE_PATH))
        page = context.new_page()

        print("🚀 開啟打卡頁面...")
        page.goto("https://pro.104.com.tw/psc2?m=b&m=b,b,b")
        page.wait_for_load_state("networkidle")

        print("🕒 嘗試立即送出打卡 API...")
        try:
            with page.expect_response(CLOCKIN_API_URL, timeout=10000) as response_info:
                page.evaluate(f'''
                    fetch("{CLOCKIN_API_URL}", {{
                        method: "POST",
                        headers: {{
                            "Content-Type": "application/json"
                        }}
                    }})
                ''')

                response = response_info.value
                json_data = response.json()

                print("📌 打卡 API 回應：", json_data)

        except Exception as e:
            print("❌ 打卡 API 發送失敗：", e)

        context.close()
        browser.close()

if __name__ == "__main__":
    clockin_test_fullflow()

























