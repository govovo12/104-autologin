from typing import Tuple, Any
from clockin_bot.tools.email.gmail_verification import get_gmail_service_async, get_latest_message_time_async
from clockin_bot.tools.common.result_code import ResultCode
from datetime import datetime, timezone, timedelta

async def step_5_fetch_latest_email_time(
    debug: bool = False
) -> Tuple[int, Any, int]:
    """
    任務模組：建立 Gmail 服務並抓最新一封信的時間戳

    Returns:
        Tuple[錯誤碼(int), service物件, 最新信時間戳秒(int)]
    """
    try:
        service = await get_gmail_service_async()
        timestamp_sec = await get_latest_message_time_async(service)
        if debug:
            dt_tw = datetime.fromtimestamp(timestamp_sec, tz=timezone(timedelta(hours=8)))
            print(f"[DEBUG] 最新信時間戳（秒）：{timestamp_sec}（台灣時間：{dt_tw.strftime('%Y-%m-%d %H:%M:%S')}）")
        return ResultCode.SUCCESS, service, timestamp_sec

    except Exception as e:
        if debug:
            print(f"[ERROR] 抓最新信時間戳失敗: {e}")
        return ResultCode.TOOLS_TASK_FETCH_VERIFICATION_CODE_FAILED, None, 0
