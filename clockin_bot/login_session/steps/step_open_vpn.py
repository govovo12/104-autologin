from clockin_bot.vpn.vpn_controller import ensure_vpn_ready
from clockin_bot.clockin.base.result import ResultCode as ClockinResult
from clockin_bot.tools.common.result_code import ResultCode  # 👈 改成統一錯誤碼系統
from clockin_bot.tools.printer.log_helper import log_code_message
import asyncio

async def step_2_open_vpn(context_data: dict) -> int:
    if not context_data.get("ENABLE_VPN", False):
        print("⛔ STEP 2: VPN 開關為 false，略過啟動")
        return ResultCode.SUCCESS

    print("🌐 STEP 2: 嘗試啟動 VPN（連線 Shadowsocks）...")
    result = await asyncio.to_thread(ensure_vpn_ready)

    # 🎯 錯誤碼轉換（只處理你關心的錯誤碼）
    if result.code == ClockinResult.VPN_START_TIMEOUT:
        code = ResultCode.TASK_VPN_START_TIMEOUT
    else:
        code = ResultCode.SUCCESS

    log_code_message(code)
    return code
