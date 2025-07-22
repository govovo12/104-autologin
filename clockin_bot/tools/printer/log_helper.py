# clockin_bot/tools/printer/log_helper.py

from clockin_bot.tools.common.result_code import (
    ResultCode,
    SUCCESS_CODES,
    TASK_ERROR_CODES,
    TOOL_ERROR_CODES,
    ERROR_MESSAGES,
)


def log_code_message(code: int):
    """根據錯誤碼印出統一格式訊息：code:xxxx <類別> msg:<訊息>"""
    if code in SUCCESS_CODES:
        category = "success"
    elif code in TASK_ERROR_CODES:
        category = "taskerror"
    elif code in TOOL_ERROR_CODES:
        category = "toolerror"
    else:
        category = "unknown"

    msg = ERROR_MESSAGES.get(code, "未知錯誤")
    print(f"code:{code} {category} msg:{msg}")
