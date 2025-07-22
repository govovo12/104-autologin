from clockin_bot.vpn.vpn_controller import stop_vpn

def step_close_vpn() -> int:
    """
    STEP（靜默）：關閉 VPN，嘗試結束 sslocal.exe。
    由子控統一處理是否 log 出錯誤碼。
    """
    result = stop_vpn()
    return result.code
