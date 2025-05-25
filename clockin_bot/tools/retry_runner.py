from clockin_bot.logger.decorators import log_call
from clockin_bot.clockin.base.result import TaskResult, ResultCode
import time
from typing import Callable, Any, Optional


@log_call
def run_with_retry(
    func: Callable[..., TaskResult],
    args: tuple = (),
    kwargs: Optional[dict] = None,
    retry: int = 3,
    delay_sec: int = 0
) -> TaskResult:
    """
    執行指定函式，若失敗則重試，最多 retry 次。

    :param func: 要執行的函式，需回傳 TaskResult
    :param args: 傳給函式的位置參數
    :param kwargs: 傳給函式的關鍵字參數
    :param retry: 最大重試次數（含第一次）
    :param delay_sec: 每次失敗後等待秒數（預設 0）
    :return: 最終一次呼叫的 TaskResult
    """
    if kwargs is None:
        kwargs = {}

    for attempt in range(1, retry + 1):
        result = func(*args, **kwargs)

        if result.code == ResultCode.SUCCESS:
            return result

        if attempt < retry:
            time.sleep(delay_sec)

    return result  # 回傳最後一次失敗結果
