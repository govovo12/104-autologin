# test_login_state.py
from playwright.sync_api import sync_playwright
from config import STORAGE_STATE_PATH

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context(storage_state=STORAGE_STATE_PATH)
    page = context.new_page()
    
    print("🔍 打開104企業大師，檢查是否直接登入...")
    page.goto("https://pro.104.com.tw/psc2?m=b&m=b,b,b")
    page.wait_for_timeout(5000)

    input("✅ 如果看到已登入畫面（可以點私人秘書），就按Enter關閉測試...")
    
    browser.close()
