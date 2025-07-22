from playwright.async_api import async_playwright, Page, Browser, BrowserContext
from clockin_bot.tools.common.result_code import ResultCode


async def step_3_open_browser(headless: bool = True) -> tuple[int, dict]:
    """
    Step 3：初始化 Playwright 瀏覽器並建立 browser/context/page。
    不印 log、不讀 .env，由子控傳入 headless 參數。

    Args:
        headless (bool): 是否使用無頭模式（由子控傳入）

    Returns:
        Tuple[int, dict]: 
            - 錯誤碼（ResultCode）
            - 成功時回傳包含 playwright、browser、context、page 的 dict，否則為空 dict
    """
    try:
        playwright = await async_playwright().start()
        browser: Browser = await playwright.chromium.launch(headless=headless)
        context: BrowserContext = await browser.new_context()
        page: Page = await context.new_page()

        return ResultCode.SUCCESS, {
            "playwright": playwright,
            "browser": browser,
            "context": context,
            "page": page
        }

    except Exception:
        return ResultCode.TASK_BROWSER_LAUNCH_FAILED, {}
