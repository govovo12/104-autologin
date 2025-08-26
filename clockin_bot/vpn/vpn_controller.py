# clockin_bot/vpn/vpn_controller.py

from clockin_bot.vpn.vpn_env_checker import check_vpn_env_vars
from clockin_bot.vpn.vpn_operator import start_vpn, stop_vpn
from clockin_bot.tools.env_loader import get_env_var, get_abs_path_from_env
from clockin_bot.tools.common.result_code import ResultCode
from clockin_bot.tools.printer.log_helper import log_code_message


def run_vpn(action: str):
    """
    根據 action 執行 VPN 操作
    回傳 (result_code, detail)
    """
    # Step 1: 檢查必要環境變數
    rc, env_vars = check_vpn_env_vars()
    if rc != ResultCode.SUCCESS:
        return rc, env_vars

    # Step 2: 取出必要值
    config_path = get_abs_path_from_env("VPN_CONFIG_PATH")
    interface_name = get_env_var("VPN_INTERFACE_NAME")
    skip_ip_check = get_env_var("VPN_SKIP_IP_CHECK", "false").lower() == "true"

    # Step 3: 執行
    if action.lower() == "start":
        return start_vpn(config_path, interface_name, skip_ip_check)
    elif action.lower() == "stop":
        return stop_vpn()
    else:
        return ResultCode.TASK_VPN_INVALID_ACTION, {"action": action}


def vpn_main(action: str = "start"):
    """
    VPN 主入口，可透過 CLI 傳入 action (start/stop)
    """
    rc, detail = run_vpn(action)
    # ✅ 使用統一的 log_helper 印出
    log_code_message(rc)
    # 如果需要，也可以選擇性印出 detail（可考慮之後加到 log_helper 內）
    if detail:
        print(f"detail: {detail}")


__task_info__ = {
    "entry": vpn_main,
    "desc": "啟動或停止 VPN，並驗證環境變數"
}
