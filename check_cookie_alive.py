# check_cookie_alive.py
from playwright.sync_api import sync_playwright
from telegram_notify import send_telegram_message
from config import STORAGE_STATE_PATH
import datetime

def check_cookie_alive():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # 用無頭模式比較快
        context = browser.new_context(storage_state=STORAGE_STATE_PATH)
        page = context.new_page()

        print("🔍 檢查 login_state.json 是否有效...")
        page.goto("https://pro.104.com.tw/psc2?m=b&m=b,b,b")
        page.wait_for_timeout(5000)

        current_url = page.url
        print(f"📍 目前URL: {current_url}")

        if "login" in current_url or "bsignin.104.com.tw" in current_url:
            print("⚠️ Cookie失效，無法直接進入104系統")
            send_telegram_message("⚠️ 104 cookie失效！請手動更新 login_state.json！")
        else:
            # Cookie正常，順便回報剩餘天數（簡單估算）
            estimated_days_left = 30  # 假設一般是30天有效期
            today = datetime.date.today()
            next_expire_date = today + datetime.timedelta(days=estimated_days_left)
            days_left = (next_expire_date - today).days

            send_telegram_message(f"✅ 104 cookie正常，估計還可使用 {days_left} 天！")
            print(f"✅ Cookie正常，大約還能用 {days_left} 天")

        browser.close()

if __name__ == "__main__":
    check_cookie_alive()
