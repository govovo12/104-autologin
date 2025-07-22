from clockin_bot.tools.common.result_code import ResultCode
from clockin_bot.tools.network.wait_for_cookie import wait_for_cookie_updated


async def step_10_wait_for_sid_cookie(
    context,
    domain: str,
    debug: bool = False
) -> tuple[int, dict]:
    """
    Step 10：等待 connect.sid 被設定，並回傳單一 SID 的 cookie header

    Args:
        context: Playwright 的 BrowserContext
        domain: 監聽 connect.sid 的目標網域（例如 "pro.104.com.tw"）
        debug: 是否開啟除錯模式

    Returns:
        Tuple[int, dict]: 
            - 成功：ResultCode.SUCCESS, sid_cookie_header（格式：{"Cookie": "connect.sid=..."}）
            - 失敗：TASK_SID_COOKIE_NOT_FOUND, {}
    """
    sid_cookie = await wait_for_cookie_updated(
        name="connect.sid",
        context=context,
        domain=domain,
        timeout=10
    )

    if not sid_cookie:
        if debug:
            print("[DEBUG] ❌ 未擷取到 connect.sid cookie")
        return ResultCode.TASK_SID_COOKIE_NOT_FOUND, {}

    sid_cookie_header = {"Cookie": f"{sid_cookie['name']}={sid_cookie['value']}"}
    if debug:
        print(f"[DEBUG] ✅ 擷取到 connect.sid cookie：{sid_cookie_header}")
    return ResultCode.SUCCESS, sid_cookie_header
