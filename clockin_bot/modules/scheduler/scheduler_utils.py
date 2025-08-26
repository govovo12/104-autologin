from clockin_bot.tools.utils_holiday import is_today_holiday
from clockin_bot.clockin.base.result import TaskResult, ResultCode
from clockin_bot.logger.decorators import log_call
from clockin_bot.logger.logger import get_logger

log = get_logger("scheduler")

@log_call
def should_skip_today() -> TaskResult:
    """
    檢查今天是否是假日或手動排除日。
    回傳 SKIP_TODAY 表示不需執行排程。
    否則回傳 SUCCESS 表示可繼續執行。
    """
    try:
        if is_today_holiday():
            return TaskResult(
                code=ResultCode.SKIP_TODAY,   # ✅ 改成 SKIP_TODAY
                message="☀️ 今天是假日或排除日，已略過執行"
            )
        return TaskResult(
            code=ResultCode.SUCCESS,
            message="✅ 今天為工作日，可執行任務"
        )
    except Exception as e:
        return TaskResult(
            code=ResultCode.UNKNOWN_ERROR,
            message=f"檢查假日邏輯發生錯誤：{e}"
        )
