import json
from clockin_bot.clockin.base.result import TaskResult, ResultCode
from clockin_bot.logger.logger import get_logger
from clockin_bot.logger.decorators import log_call

log = get_logger("response_parser")

@log_call
def parse_clockin_response(response) -> TaskResult:
    try:
        res_json = response.json()
        log.info(f"回傳 JSON：{json.dumps(res_json, ensure_ascii=False)}")
    except Exception as e:
        return TaskResult(
            code=ResultCode.RESPONSE_PARSE_ERROR,
            message=f"回傳內容不是合法 JSON：{e}"
        )

    if res_json.get("code") != 200:
        return TaskResult(
            code=ResultCode.API_LOGIC_FAILED,
            message=f"API 回傳失敗：{res_json.get('message', '未知錯誤')}"
        )

    # ✅ 修正這裡：不要用 response.data，應該用 res_json
    att_id = res_json.get("data", {}).get("overAttCardDataId")
    if not att_id:
        return TaskResult(
            code=ResultCode.ATT_ID_MISSING,
            message="未取得打卡 ID"
        )

    return TaskResult(
        code=ResultCode.SUCCESS,
        message="成功取得打卡 ID",
        data={"att_id": att_id}
    )

__task_info__ = {
    "name": "parse_clockin_response",
    "desc": "解析打卡 API 回傳 JSON 並取出打卡 ID",
    "entry": parse_clockin_response
}
