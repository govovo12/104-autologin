from clockin_bot.tools.network.wait_for_request import wait_for_request_by_url
from clockin_bot.tools.common.result_code import ResultCode


async def step_9_wait_for_redirect(page, debug: bool = False) -> int:
    """
    Step 9：等待登入成功導向 /psc2

    Args:
        page (playwright.async_api.Page): Playwright 的 page 實例
        debug (bool): 是否開啟除錯模式

    Returns:
        int: ResultCode.SUCCESS 表示導向成功；
             ResultCode.TOOLS_WAIT_FOR_PSC2_FAILED 表示逾時未導向
    """
    success = await wait_for_request_by_url(
        page=page,
        url_keyword="/psc2",
        timeout=10000,
        debug=debug
    )

    if not success:
        return ResultCode.TOOLS_WAIT_FOR_PSC2_FAILED

    return ResultCode.SUCCESS
