# login_save_cookie.py
from playwright.sync_api import sync_playwright
from config import STORAGE_STATE_PATH

def save_login_cookie():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        print("🔔 正在打開104登入頁，請手動輸入帳號密碼與驗證碼...")
        page.goto("https://pro.104.com.tw/psc2?m=b&m=b,b,b")
        page.wait_for_timeout(5000)  # 等5秒讓你操作

        input("✅ 完成登入後，請按 Enter 鍵繼續...")

        context.storage_state(path=STORAGE_STATE_PATH)
        print(f"📦 登入狀態已保存到 {STORAGE_STATE_PATH}")
        browser.close()

if __name__ == "__main__":
    save_login_cookie()
