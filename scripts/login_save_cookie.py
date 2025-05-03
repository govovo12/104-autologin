from playwright.sync_api import sync_playwright
from pathlib import Path

# === 設定資料夾與檔案位置（旗標路徑） ===
BASE_DIR = Path(__file__).resolve().parent.parent
STORAGE_STATE_PATH = BASE_DIR / "data" / "login_state.json"

def save_login_cookie():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        print("🔔 正在打開104私人秘書頁，請手動登入...")
        page.goto("https://pro.104.com.tw/psc2?m=b&m=b,b,b")

        page.wait_for_timeout(5000)  # 等5秒讓你操作登入

        input("✅ 完成登入後，請按 Enter 繼續...")

        context.storage_state(path=str(STORAGE_STATE_PATH))
        print(f"📦 登入狀態已保存到 {STORAGE_STATE_PATH}")

        browser.close()

if __name__ == "__main__":
    save_login_cookie()





