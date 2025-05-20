from playwright.sync_api import sync_playwright
from pathlib import Path
from clockin_bot.logger.logger import get_logger
from clockin_bot.logger.decorators import log_call

log = get_logger("login_cookie")

# 設定資料夾與檔案位置（絕對路徑）
BASE_DIR = Path(__file__).resolve().parent.parent
STORAGE_STATE_PATH = BASE_DIR / "data" / "login_state.json"

@log_call
def save_login_cookie():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        log.info("開啟104私人秘書頁面，請完成登入...")
        page.goto("https://pro.104.com.tw/psc2?m=b&m=b,b,b")
        page.wait_for_timeout(5000)

        input("登入完成後請按 Enter 繼續...")

        context.storage_state(path=str(STORAGE_STATE_PATH))
        log.info(f"登入狀態已保存至 {STORAGE_STATE_PATH}")

        browser.close()

if __name__ == "__main__":
    save_login_cookie()







