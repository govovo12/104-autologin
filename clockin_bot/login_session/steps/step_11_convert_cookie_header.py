from clockin_bot.tools.common.result_code import ResultCode
from clockin_bot.tools.network.cookie_helper import (
    fetch_browser_cookies,
    convert_cookies_to_header,
)


async def step_11_convert_cookie_header(
    context,
    debug: bool = False
) -> tuple[int, dict]:
    """
    Step 11：從瀏覽器抓取 cookies，轉換為 header 格式並回傳 login_state

    Args:
        context: Playwright 的 BrowserContext 實例
        debug: 是否開啟除錯模式

    Returns:
        Tuple[int, dict]: 
            - 成功：ResultCode.SUCCESS, login_state（格式：{"Cookie": "..."}）
            - 失敗：TASK_CONVERT_COOKIE_HEADER_FAILED, {}
    """
    try:
        cookies = await fetch_browser_cookies(context)
        if debug:
            print(f"[DEBUG] 抓取到 cookies：{cookies}")

        login_state = convert_cookies_to_header(cookies)
        if debug:
            print(f"[DEBUG] 轉換為 header：{login_state}")

        return ResultCode.SUCCESS, login_state

    except Exception as e:
        if debug:
            print(f"[DEBUG] ❌ Cookie 轉換失敗：{e}")
        return ResultCode.TASK_CONVERT_COOKIE_HEADER_FAILED, {}
