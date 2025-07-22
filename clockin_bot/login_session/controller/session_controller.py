import asyncio

# ✅ 錯誤碼與 log 工具（共用）
from clockin_bot.tools.common.result_code import ResultCode
from clockin_bot.tools.printer.log_helper import log_code_message

# ✅ 任務模組（登入步驟）
from clockin_bot.login_session.steps.load_env_config import step_1_load_env
from clockin_bot.login_session.steps.step_open_vpn import step_2_open_vpn
from clockin_bot.login_session.steps.step_3_open_browser import step_3_open_browser
from clockin_bot.login_session.steps.step_4_navigate_to_login import step_4_navigate_to_login
from clockin_bot.login_session.steps.step_close_vpn import step_close_vpn
from clockin_bot.login_session.steps.step_6_submit_login import step_6_submit_login
from clockin_bot.login_session.steps.step_5_fetch_latest_email_time import step_5_fetch_latest_email_time
from clockin_bot.login_session.steps.step_7_fetch_verification_code import step_7_fetch_verification_code
from clockin_bot.login_session.steps.step_8_input_verification_code import step_8_input_verification_code
from clockin_bot.login_session.steps.step_9_wait_for_redirect import step_9_wait_for_redirect
from clockin_bot.login_session.steps.step_10_wait_for_sid_cookie import step_10_wait_for_sid_cookie
from clockin_bot.login_session.steps.step_11_convert_cookie_header import step_11_convert_cookie_header
from clockin_bot.login_session.steps.step_12_save_login_state import save_login_state
from clockin_bot.login_session.steps.step_13_release_playwright import run_step_13_release_playwright




# Step 1：讀取 .env 並存入 context_data
async def run_step_1_load_env(context_data: dict) -> int:
    print("🚪 STEP 1: 讀取環境參數")
    code, env_data = await step_1_load_env()
    if code != ResultCode.SUCCESS:
        log_code_message(code)
        return code
    context_data.update(env_data)
    return ResultCode.SUCCESS


# Step 2：開啟 VPN（根據 ENABLE_VPN 決定）
async def run_step_2_open_vpn(context_data: dict) -> int:
    print("🌐 STEP 2: 嘗試開啟 VPN（若設定為啟用）")
    code = await step_2_open_vpn(context_data)
    if code != ResultCode.SUCCESS:
        log_code_message(code)
        return code
    return ResultCode.SUCCESS


# Step 3：初始化瀏覽器與 page
async def run_step_3_open_browser(context_data: dict) -> int:
    print("🧱 STEP 3: 初始化瀏覽器與分頁")
    headless = context_data.get("HEADLESS_MODE", True)
    code, browser_data = await step_3_open_browser(headless=headless)
    log_code_message(code)
    if code != ResultCode.SUCCESS:
        return code
    context_data.update(browser_data)
    return ResultCode.SUCCESS


# Step 4：導航至登入頁
async def run_step_4_navigate_to_login(context_data: dict) -> int:
    print("🧭 STEP 4: 導航前往登入頁")
    code = await step_4_navigate_to_login(
        page=context_data.get("page"),
        url=context_data.get("LOGIN_URL"),
        debug=context_data.get("DEBUG_MODE", False)
    )
    log_code_message(code)
    return code

# Step 5：抓最新 Gmail 驗證碼（不等待新信）
async def run_step_5_fetch_latest_email_time(context_data: dict) -> int:
    print("📧 STEP 5: 抓取最新信時間戳")

    # 這裡不自己建立 service，全部交給任務模組做
    code, service, last_email_time = await step_5_fetch_latest_email_time(
        debug=context_data.get("DEBUG_MODE", False)
    )

    log_code_message(code)
    if code != ResultCode.SUCCESS:
        return code

    context_data["gmail_service"] = service
    context_data["last_email_time"] = last_email_time

    if context_data.get("DEBUG_MODE", False):
        print(f"[DEBUG] context_data after step 5: {context_data}")

    return ResultCode.SUCCESS



# Step 6：提交帳密登入
async def run_step_6_submit_login(context_data: dict) -> int:
    print("🔐 STEP 6: 提交帳密登入")
    code = await step_6_submit_login(
        page=context_data.get("page"),
        account=context_data.get("ACCOUNT"),
        password=context_data.get("PASSWORD"),
        debug=context_data.get("DEBUG_MODE", False)
    )
    log_code_message(code)
    return code

# Step 7：抓取最新信件的驗證碼
async def run_step_7_fetch_verification_code(context_data: dict) -> int:
    print("📧 STEP 7: 抓取驗證碼信")
    code, verification_code = await step_7_fetch_verification_code(
        service=context_data.get("gmail_service"),
        newer_than=context_data.get("last_email_time", 0),
        timeout_sec=60,
        debug=context_data.get("DEBUG_MODE", False)
    )
    log_code_message(code)
    if code != ResultCode.SUCCESS:
        return code
    context_data["verification_code"] = verification_code
    if context_data.get("DEBUG_MODE", False):
        print(f"[DEBUG] context_data after step 7: {context_data}")
    return ResultCode.SUCCESS

# Step 8：輸入驗證碼
async def run_step_8_input_verification_code(context_data: dict) -> int:
    print("⌨️ STEP 8: 輸入驗證碼")
    code = await step_8_input_verification_code(
        page=context_data["page"],
        verification_code=context_data["verification_code"],
        debug=context_data.get("DEBUG_MODE", False)
    )
    log_code_message(code)
    return code

# Step 9：等待跳轉至私人秘書頁面
async def run_step_9_wait_for_redirect(context_data: dict) -> int:
    print("🛰️ STEP 9: 等待導向 /psc2")
    code = await step_9_wait_for_redirect(
        page=context_data["page"],
        debug=context_data.get("DEBUG_MODE", False)
    )
    log_code_message(code)
    return code

# Step 10：抓取最新的sid用來確認伺服器已準備好最新cookie
async def run_step_10_wait_for_sid_cookie(context_data: dict) -> int:
    print("🍪 STEP 10: 等待 connect.sid cookie")
    code, sid_cookie_header = await step_10_wait_for_sid_cookie(
        context=context_data["context"],
        domain=context_data["COOKIE_DOMAIN"],
        debug=context_data.get("DEBUG_MODE", False)
    )
    log_code_message(code)
    if code != ResultCode.SUCCESS:
        return code

    context_data["sid_cookie_header"] = sid_cookie_header
    return ResultCode.SUCCESS

# Step 11：抓取原始cookie並轉換為 header
async def run_step_11_convert_cookie_header(context_data: dict) -> int:
    print("📦 STEP 11: 擷取 cookies 並轉換為 header")
    code, login_state = await step_11_convert_cookie_header(
        context=context_data["context"],
        debug=context_data.get("DEBUG_MODE", False)
    )
    log_code_message(code)
    if code != ResultCode.SUCCESS:
        return code

    context_data["login_state"] = login_state
    return ResultCode.SUCCESS

# Step 12：儲存 login_state 檔案
async def run_step_12_save_login_state(context_data: dict) -> int:
    print("📦 STEP 12: 儲存 login_state 檔案")
    code = await save_login_state(
        login_state=context_data["login_state"],
        save_path=context_data["COOKIE_SAVE_PATH"],
        debug=context_data.get("DEBUG_MODE", False)
    )
    log_code_message(code)
    return code

# Step 13：釋放 Playwright 資源
async def run_step_13_release_playwright_step(context_data: dict) -> int:
    print("📦 STEP 13: 關閉 Playwright 資源")
    code, _ = await run_step_13_release_playwright(context_data)
    return code



# VPN 關閉模組（尚未指定 Step 編號，未來可調整）
async def run_step_close_vpn(context_data: dict) -> int:
    # 暫不印 STEP N，未來再補
    code = await asyncio.to_thread(step_close_vpn)
    log_code_message(code)
    return code


# ✅ 子控主流程
async def run_session_controller():
    context_data = {}

    code = await run_step_1_load_env(context_data)
    if code != ResultCode.SUCCESS:
        return

    code = await run_step_2_open_vpn(context_data)
    if code != ResultCode.SUCCESS:
        return

    code = await run_step_3_open_browser(context_data)
    if code != ResultCode.SUCCESS:
        return

    code = await run_step_4_navigate_to_login(context_data)
    if code != ResultCode.SUCCESS:
        return
    
    code = await run_step_5_fetch_latest_email_time(context_data)
    if code != ResultCode.SUCCESS:
        return
    code = await run_step_6_submit_login(context_data)
    if code != ResultCode.SUCCESS:
        return
    
    code = await run_step_7_fetch_verification_code(context_data)
    if code != ResultCode.SUCCESS:
        return
    
    code = await run_step_8_input_verification_code(context_data)
    if code != ResultCode.SUCCESS:
        return
    
    code = await run_step_9_wait_for_redirect(context_data)
    if code != ResultCode.SUCCESS:
        return
    
    code = await run_step_10_wait_for_sid_cookie(context_data)
    if code != ResultCode.SUCCESS:
        return

    code = await run_step_11_convert_cookie_header(context_data)
    if code != ResultCode.SUCCESS:
        return

    code = await run_step_12_save_login_state(context_data)
    if code != ResultCode.SUCCESS:
        return

    code = await run_step_13_release_playwright_step(context_data)
    if code != ResultCode.SUCCESS:
        return



    code = await run_step_close_vpn(context_data)
    if code != ResultCode.SUCCESS:
        return

 

    print("🎉 登入流程全部完成！")


# ✅ 提供 CLI 入口
__task_info__ = {
    "entry": lambda: asyncio.run(run_session_controller()),
    "desc": "登入流程控制器（使用 .env 自動登入）"
}
