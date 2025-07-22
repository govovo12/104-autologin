from typing import Tuple
from clockin_bot.tools.common.result_code import ResultCode
from clockin_bot.tools.email.gmail_verification import fetch_gmail_verification_code_with_debug_async

async def step_7_fetch_verification_code(
    service,
    newer_than: int,
    timeout_sec: int = 60,
    debug: bool = False
) -> Tuple[int, str]:
    """
    Step 7：抓晚於 newer_than 的 Gmail 驗證碼信（非同步版）

    Args:
        service: Gmail API 非同步服務物件
        newer_than: 查詢該時間戳（秒）之後的信件
        timeout_sec: 最大等待時間（秒）
        debug: 是否印出除錯資訊

    Returns:
        Tuple[int, str]: (錯誤碼, 驗證碼字串)，失敗驗證碼為空字串
    """
    try:
        code = await fetch_gmail_verification_code_with_debug_async(
            service=service,
            newer_than=newer_than,
            timeout_sec=timeout_sec,
            debug=debug
        )
        return ResultCode.SUCCESS, code
    except Exception:
        return ResultCode.TOOLS_TASK_FETCH_VERIFICATION_CODE_FAILED, ""
