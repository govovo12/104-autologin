from clockin_bot.session.login_save_cookie import save_cookie_by_login
from clockin_bot.session.convert_login_cookie import convert_login_state_to_cookie_header
from clockin_bot.logger.logger import get_logger
from clockin_bot.logger.decorators import log_call
from clockin_bot.clockin.base.result import TaskResult, ResultCode

log = get_logger("login_convert_flow")

@log_call
def login_and_convert():
    log.info("🚀 開始執行登入 + cookie 轉換流程")

    login_result = save_cookie_by_login()
    if login_result.code != ResultCode.SUCCESS:
        log.error(f"❌ 登入失敗：{login_result.message}")
        return TaskResult(code=ResultCode.LOGIN_FAILED, message="登入失敗，無法轉換 cookie")

    convert_result = convert_login_state_to_cookie_header()
    if convert_result.code != ResultCode.SUCCESS:
        log.error(f"⚠ Cookie 轉換失敗：{convert_result.message}")
        return TaskResult(code=ResultCode.COOKIE_PARSE_ERROR, message="登入成功但轉換 cookie 失敗")

    return TaskResult(code=ResultCode.SUCCESS, message="✅ 登入 + cookie 轉換成功")

__task_info__ = {
    "name": "login_convert",
    "desc": "一條龍執行：登入 + 轉換 cookie_header",
    "entry": login_and_convert,
}
