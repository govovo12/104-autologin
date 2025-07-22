import asyncio
import time
from playwright.async_api import async_playwright

from clockin_bot.login_session.fetch_verification_code import (
    get_gmail_service,
    fetch_gmail_verification_code,
)
from clockin_bot.login_session.input_verification_code import input_verification_code
from clockin_bot.login_session.submit_login_form import submit_login_form
from clockin_bot.tools.network.wait_for_request import wait_for_request_by_url
from clockin_bot.tools.network.cookie_helper import (
    convert_cookies_to_header,
    save_cookies_to_file,
    save_headers_to_file,
)
from clockin_bot.tools.network.wait_for_cookie import wait_for_cookie_updated
from clockin_bot.tools.debug.sid_tracker import track_sid_event
from clockin_bot.tools.env_loader import get_env_var


# 開關
KEEP_BROWSER_OPEN = False
SAVE_AS_HEADER = True
DEBUG = get_env_var("DEBUG_MODE", "false").lower() == "true"

LOGIN_URL = "https://pro.104.com.tw/psc2"
ACCOUNT = "bs10125@bravostargames.com"
PASSWORD = "zxcv1325"


def track_sid_updates(context):
    """
    若 DEBUG_MODE 開啟，追蹤 sid 被設定的來源與值。
    """
    sid_values = set()

    async def handle_response(response):
        try:
            headers = await response.all_headers()
            set_cookie = headers.get("set-cookie", "")
            if "connect.sid=" in set_cookie:
                sid_value = set_cookie.split("connect.sid=")[1].split(";")[0]
                if sid_value not in sid_values:
                    track_sid_event(response.url, sid_value)
                    sid_values.add(sid_value)
        except Exception as e:
            print(f"[Error] sid 解析錯誤：{e}")

    if DEBUG:
        context.on("response", handle_response)


async def run():
    print("🚪 [Step 1] 啟動登入流程")

    playwright = await async_playwright().start()
    HEADLESS = get_env_var("HEADLESS_MODE", "false").lower() == "true"
    browser = await playwright.chromium.launch(headless=HEADLESS)
    context = await browser.new_context()

    track_sid_updates(context)
    page = await context.new_page()

    print("🚀 前往登入入口...")
    await page.goto(LOGIN_URL, timeout=0)

    # ✅ Step 1: 自動輸入帳密 + 點擊登入
    raw_timestamp = int(time.time())
    newer_than = raw_timestamp - 60
    print(f"[DEBUG] 帳密填完時間戳（原始）：{raw_timestamp}")
    print(f"[DEBUG] 寬容後作為比對時間戳：{newer_than}")

    await submit_login_form(page, ACCOUNT, PASSWORD)

    print("🛰️ [Step 2] 等待帳密登入封包送出")
    await wait_for_request_by_url(page, "/oauth2/login", method="POST", timeout=10000)

    print("📥 建立 Gmail 服務...")
    service = get_gmail_service()

    print("📥 擷取 Gmail 驗證碼信件...")
    code = fetch_gmail_verification_code(
        service=service,
        newer_than=newer_than,
        timeout_sec=60,
    )

    print(f"[DEBUG] 收到模組驗證碼：{code}")

    print("🔡 開始輸入驗證碼...")
    await input_verification_code(page, code)

    print("🛰️ 等待登入成功導向 /psc2")
    await wait_for_request_by_url(page, "/psc2", timeout=10000)
    print("✅ 偵測到登入成功導向 /psc2")

    # ✅ 等待 sid 被替換為最終登入版本
    sid_cookie = await wait_for_cookie_updated("connect.sid", context, domain="pro.104.com.tw", timeout=10)
    if sid_cookie:
        print(f"[DEBUG] connect.sid 抓到了 ✅：{sid_cookie['value']}")
    else:
        print("[WARNING] ❌ 最終 cookie 清單仍無 connect.sid")

    # Step 4: 擷取完整 cookies 並轉換 header
    cookies = await context.cookies()
    headers = convert_cookies_to_header(cookies)
    print(f"[DEBUG] Header 已準備好：{headers}")

    save_path = "C:/Users/user/Desktop/104-autologin/clockin_bot/data/login_state.json"
    if SAVE_AS_HEADER:
        save_headers_to_file(headers, save_path)
        print("✅ Header 已儲存 login_state.json（格式：header）")
    else:
        save_cookies_to_file(cookies, save_path)
        print("✅ Cookie list 已儲存 login_state.json（格式：cookie list）")

    if KEEP_BROWSER_OPEN:
        print("✅ 登入流程結束，瀏覽器將保持開啟")
        await asyncio.sleep(3600)
    else:
        await browser.close()
        await playwright.stop()


def session_controller():
    asyncio.run(run())


__task_info__ = {
    "entry": session_controller,
    "desc": "登入 + 驗證碼流程（自動輸入帳密 + 偵測登入成功 + 擷取 Cookie）"
}
