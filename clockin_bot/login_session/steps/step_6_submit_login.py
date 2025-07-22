# workspace/modules/clockin/step_6_submit_login.py

from playwright.async_api import Page
from clockin_bot.tools.common.result_code import ResultCode
from clockin_bot.tools.network.wait_for_request import wait_for_request_by_url


async def step_6_submit_login(
    page: Page,
    account: str,
    password: str,
    debug: bool = False
) -> int:
    """
    Step 6：提交登入表單並等待登入封包送出（優化穩定版）

    Args:
        page (Page): Playwright 的頁面物件。
        account (str): 登入帳號。
        password (str): 登入密碼。
        debug (bool): 是否開啟 debug 模式（錯誤時截圖）。

    Returns:
        int: 結果錯誤碼。
    """
    try:
        await page.wait_for_url("**/login**", timeout=20000)

        # Step 1: 填入帳號
        account_selectors = ["#username", "input[type='text']", "input[type='email']"]
        for selector in account_selectors:
            try:
                await page.wait_for_selector(selector, timeout=5000)
                await page.fill(selector, account)
                break
            except:
                continue
        else:
            if debug:
                await page.screenshot(path="debug_no_username.png")
            return ResultCode.TASK_SUBMIT_LOGIN_FAILED

        # Step 2: 填入密碼
        password_selectors = ["#password", "input[type='password']"]
        for selector in password_selectors:
            try:
                await page.wait_for_selector(selector, timeout=5000)
                await page.fill(selector, password)
                break
            except:
                continue
        else:
            if debug:
                await page.screenshot(path="debug_no_password.png")
            return ResultCode.TASK_SUBMIT_LOGIN_FAILED

        # Step 3: 點擊登入按鈕（多種選擇器）
        button_selectors = [
            'text=立即登入',
            'button:has-text("立即登入")',
            'text=登入',
            'button[type="submit"]'
        ]
        for selector in button_selectors:
            try:
                btn = await page.query_selector(selector)
                if btn:
                    await btn.click()
                    break
            except:
                continue
        else:
            if debug:
                await page.screenshot(path="debug_no_loginbtn.png")
            return ResultCode.TASK_SUBMIT_LOGIN_FAILED

        # Step 4: 等待登入封包送出
        success = await wait_for_request_by_url(
            page=page,
            url_keyword="/oauth2/login",
            method="POST",
            timeout=10000
        )
        if not success:
            if debug:
                await page.screenshot(path="debug_login_request_timeout.png")
            return ResultCode.TASK_SUBMIT_LOGIN_FAILED

        # Step 5: 等待畫面穩定
        await page.wait_for_timeout(1000)
        return ResultCode.SUCCESS

    except Exception:
        if debug:
            await page.screenshot(path="debug_submit_login_generic.png")
        return ResultCode.TASK_SUBMIT_LOGIN_FAILED
