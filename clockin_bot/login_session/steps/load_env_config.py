import os
from pathlib import Path
from dotenv import load_dotenv
from clockin_bot.tools.common.result_code import ResultCode
from clockin_bot.tools.printer.log_helper import log_code_message


async def step_1_load_env() -> tuple[int, dict]:
    """
    Step 1：讀取 .env 並回傳所需欄位（不直接修改 context_data）
    - 缺少欄位時回傳錯誤碼
    - 若 DEBUG_MODE 開啟，會印出讀到的參數與成功訊息
    """
    env_path = Path(__file__).resolve().parents[2] / ".env"
    load_dotenv(env_path)

    env_data = {
        "ACCOUNT": os.getenv("LOGIN_ACCOUNT"),
        "PASSWORD": os.getenv("LOGIN_PASSWORD"),
        "LOGIN_URL": os.getenv("LOGIN_URL"),

        "HEADLESS_MODE": os.getenv("HEADLESS_MODE", "true").lower() == "true",
        "DEBUG_MODE": os.getenv("DEBUG_MODE", "false").lower() == "true",
        "DEBUG_SID_TRACKER": os.getenv("ENABLE_SID_TRACKER", "false").lower() == "true",
        "ENABLE_VPN": os.getenv("ENABLE_VPN", "false").lower() == "true",

        "COOKIE_NAME": os.getenv("COOKIE_NAME", "connect.sid"),
        "COOKIE_DOMAIN": os.getenv("COOKIE_DOMAIN", "pro.104.com.tw"),
        "COOKIE_SAVE_PATH": os.getenv(
            "COOKIE_SAVE_PATH",
            "C:/Users/user/Desktop/104-autologin/clockin_bot/data/login_state.json"
        ),
    }

    required_keys = ["ACCOUNT", "PASSWORD", "LOGIN_URL"]
    for key in required_keys:
        if not env_data.get(key):
            return ResultCode.TASK_LOAD_ENV_MISSING_KEY, {}

    if env_data["DEBUG_MODE"]:
        print("[step_1_load_env] 讀取到的 .env 設定：")
        for k, v in env_data.items():
            print(f"  {k}: {v}")
        log_code_message(ResultCode.SUCCESS)

    return ResultCode.SUCCESS, env_data
