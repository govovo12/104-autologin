# clockin_bot/vpn/vpn_env_checker.py

from clockin_bot.tools.env_loader import get_all_env_vars
from clockin_bot.tools.common.result_code import ResultCode

# VPN 啟動必需的 .env Key
REQUIRED_VPN_KEYS = [
    "VPN_CONFIG_PATH",
    "VPN_INTERFACE_NAME",
    "VPN_SKIP_IP_CHECK"
]

def check_vpn_env_vars():
    """
    檢查 VPN 相關的 .env key 是否齊全
    回傳 (result_code, detail)
    - 成功: (ResultCode.SUCCESS, env_vars)
    - 失敗: (ResultCode.TASK_VPN_ENV_MISSING_KEY, {"missing": [...]})
    """
    env_vars = get_all_env_vars()
    missing = [key for key in REQUIRED_VPN_KEYS if not env_vars.get(key)]

    if missing:
        return ResultCode.TASK_VPN_ENV_MISSING_KEY, {"missing": missing}

    return ResultCode.SUCCESS, env_vars
