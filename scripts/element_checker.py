from pathlib import Path
from playwright.sync_api import sync_playwright

# === 旗標路徑設定 ===
BASE_DIR = Path(__file__).resolve().parent.parent
STORAGE_STATE_PATH = BASE_DIR / "data" / "login_state.json"

def check_clockin_elements():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(storage_state=str(STORAGE_STATE_PATH))
        page = context.new_page()

        print("🌐 開啟私人秘書打卡頁...")
        page.goto("https://pro.104.com.tw/psc2?m=b&m=b,b,b")
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(3000)

        print("🧪 開始列出所有提示元素...")
        try:
            elements = page.locator("._2_body").all_inner_texts()
            for idx, text in enumerate(elements):
                print(f"[{idx}] {text}")

            print("\n🎯 篩選出包含「打卡成功」的元素：")
            success_elements = [text for text in elements if "打卡成功" in text]
            if success_elements:
                for text in success_elements:
                    print(f"✅ 找到：{text}")
            else:
                print("❌ 沒找到任何『打卡成功』提示。")
        except Exception as e:
            print(f"❌ 抓提示內容時錯誤: {e}")

        page.close()
        context.close()
        browser.close()

if __name__ == "__main__":
    check_clockin_elements()

