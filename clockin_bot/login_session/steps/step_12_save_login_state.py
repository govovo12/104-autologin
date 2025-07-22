"""
Step 12：儲存 login_state 到指定檔案

This task writes the login_state dictionary to the given save_path
as JSON. It is typically called after cookie conversion.
"""

import json
from clockin_bot.tools.common.result_code import ResultCode


async def save_login_state(login_state: dict, save_path: str, debug: bool = False) -> int:
    """
    Save login_state (e.g., {"Cookie": "..."} dict) to the specified path as JSON.

    Args:
        login_state (dict): Cookie header dictionary.
        save_path (str): Absolute path to write the login_state.
        debug (bool): If True, prints confirmation of save.

    Returns:
        int: ResultCode.SUCCESS on success, or TASK_SAVE_LOGIN_STATE_FAILED on failure.
    """
    try:
        with open(save_path, "w", encoding="utf-8") as f:
            json.dump(login_state, f, ensure_ascii=False, indent=2)

        if debug:
            print(f"[DEBUG] login_state saved to {save_path}")
            print(f"[DEBUG] content: {login_state}")

        return ResultCode.SUCCESS
    except Exception:
        return ResultCode.TASK_SAVE_LOGIN_STATE_FAILED
