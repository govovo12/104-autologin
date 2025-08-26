import requests
from clockin_bot.clockin.base.result import TaskResult, ResultCode
from clockin_bot.logger.logger import get_logger
from clockin_bot.logger.decorators import log_call

log = get_logger("clockin_api")

CLOCKIN_URL = "https://pro.104.com.tw/psc2/api/f0400/newClockin"

@log_call
def send_clockin_request(headers: dict) -> TaskResult:
    try:
        response = requests.post(
            CLOCKIN_URL,
            headers=headers,
            timeout=10  # ✅ 移除 proxies=PROXIES，直接用系統路由
        )
        log.info(f"HTTP 狀態碼：{response.status_code}")

        return TaskResult(
            code=ResultCode.SUCCESS,
            message="成功取得 API 回應",
            data=response
        )

    except Exception as e:
        return TaskResult(
            code=ResultCode.API_REQUEST_EXCEPTION,
            message=f"打卡請求發生例外：{e}"
        )

__task_info__ = {
    "name": "send_clockin_request",
    "desc": "直接發送 104 打卡 API 並回傳 response 結果（使用系統網路）",
    "entry": send_clockin_request
}
