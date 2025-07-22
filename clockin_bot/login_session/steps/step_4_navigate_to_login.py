# clockin_bot/login_session/steps/step3_navigate_to_login.py

from playwright.async_api import Page, TimeoutError as PlaywrightTimeoutError
from clockin_bot.tools.common.result_code import ResultCode

async def step_4_navigate_to_login(page: Page, url: str, debug: bool) -> int:
    """
    Step 3：開啟登入頁面。
    嘗試以 Playwright 導航至指定登入網址，並回傳對應錯誤碼。
    """
    try:
        if debug:
            print(f"[DEBUG] 導航前往登入頁：{url}")
        await page.goto(url, timeout=60000)
        if debug:
            print("[DEBUG] 導航成功：頁面已載入完成")
        return ResultCode.SUCCESS
    except PlaywrightTimeoutError:
        if debug:
            print("[DEBUG] 導航失敗：timeout")
        return ResultCode.TASK_NAVIGATE_FAILED
    except Exception as e:
        if debug:
            print(f"[DEBUG] 導航失敗：{e}")
        return ResultCode.TASK_NAVIGATE_FAILED
