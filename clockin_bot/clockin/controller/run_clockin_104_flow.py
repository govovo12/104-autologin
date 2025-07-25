from clockin_bot.clockin.cookie_loader import load_login_state
from clockin_bot.clockin.clockin_api import send_clockin_request
from clockin_bot.clockin.response_parser import parse_clockin_response
from clockin_bot.clockin.base.result import TaskResult, ResultCode
from clockin_bot.logger.logger import get_logger
from clockin_bot.logger.decorators import log_call

log = get_logger("clockin_ctrl")


@log_call
def run_clockin_104_flow() -> TaskResult:
    log.info("[CTRL] 開始執行 104 打卡流程 controller")

    r1 = load_login_state()
    if r1.code != ResultCode.SUCCESS:
        return r1

    headers = r1.data  # ✅ 相信 session_controller 已決定好格式

    r2 = send_clockin_request(headers)
    if r2.code != ResultCode.SUCCESS:
        return r2

    r3 = parse_clockin_response(r2.data)
    return r3


__task_info__ = {
    "name": "run_clockin_104_flow",
    "desc": "控制整體打卡流程：讀取 login_state.json（已是 header）→ 發送 API → 解析結果",
    "entry": run_clockin_104_flow
}
