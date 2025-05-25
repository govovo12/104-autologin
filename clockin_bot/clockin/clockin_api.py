import requests
from clockin_bot.clockin.base.result import TaskResult, ResultCode
from clockin_bot.logger.logger import get_logger
from clockin_bot.logger.decorators import log_call

log = get_logger("clockin_api")

PROXIES = {
    "http": "socks5h://127.0.0.1:1080",
    "https": "socks5h://127.0.0.1:1080"
}

CLOCKIN_URL = "https://pro.104.com.tw/psc2/api/f0400/newClockin"

@log_call
def send_clockin_request(headers: dict) -> TaskResult:
    try:
        #log.info(f"送出的 Cookie: {headers.get('cookie')}")

        response = requests.post(
            CLOCKIN_URL,
            headers=headers,
            proxies=PROXIES,
            timeout=10
        )
        log.info(f"HTTP 狀態碼：{response.status_code}")

        # 不要這邊就 json()，讓 parser 處理
        return TaskResult(
            code=ResultCode.SUCCESS,
            message="成功取得 API 回應",
            data=response  # ✅ 保留原始 response
        )

    except Exception as e:
        return TaskResult(
            code=ResultCode.API_REQUEST_EXCEPTION,
            message=f"打卡請求發生例外：{e}"
        )

__task_info__ = {
    "name": "send_clockin_request",
    "desc": "透過 socks5 proxy 發送 104 打卡 API 並回傳 response 結果",
    "entry": send_clockin_request
}
