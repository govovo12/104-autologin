import json
from pathlib import Path
from playwright.sync_api import sync_playwright

# === 設定資料夾與檔案位置 ===
BASE_DIR = Path(__file__).resolve().parent.parent
COOKIE_PATH = BASE_DIR / "data" / "login_state.json"

# === 自動登入並儲存 Cookie ===
def save_login_cookies():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        print("請手動登入 104 統一登入頁面...")
        page.goto("https://bsignin.104.com.tw/login")

        input("完成登入後請按 Enter 繼續...")

        cookies = context.cookies()
        with open(COOKIE_PATH, "w", encoding="utf-8") as f:
            json.dump({"cookies": cookies}, f, ensure_ascii=False, indent=2)

        print(f"✅ 已儲存 Cookie 至 {COOKIE_PATH}")
        browser.close()


if __name__ == "__main__":
    save_login_cookies()


