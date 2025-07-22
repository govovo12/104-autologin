import psutil
from clockin_bot.vpn.connect_ss_local import start_vpn
from clockin_bot.tools.retry_runner import run_with_retry
from clockin_bot.tools.log_utils import report_and_notify
from clockin_bot.clockin.base.result import TaskResult, ResultCode
from clockin_bot.logger.logger import get_logger

log = get_logger("vpn")





def ensure_vpn_ready() -> TaskResult:
    """
    啟動 VPN，並進行最多 3 次重試。
    若成功則回傳 SUCCESS，否則會自動推播錯誤訊息與 log。
    """
    result = run_with_retry(start_vpn, retry=3, delay_sec=1)

    if result.code != ResultCode.SUCCESS:
        report_and_notify(result)

    return result


def stop_vpn() -> TaskResult:
    """
    停止 VPN：嘗試結束 sslocal.exe 背景程序。
    """
    found = False
    for proc in psutil.process_iter(["pid", "name"]):
        if "sslocal.exe" in proc.info["name"]:
            try:
                proc.terminate()
                found = True
            except Exception as e:
                msg = f"❌ 結束 sslocal.exe 失敗：{e}"
                log.error(msg)
                return TaskResult(code=ResultCode.VPN_STOP_FAILED, message=msg)

    if found:
        msg = "✅ VPN (sslocal.exe) 已成功結束"
        log.info(msg)
        return TaskResult(code=ResultCode.SUCCESS, message=msg)
    else:
        msg = "⚠ 找不到正在執行的 sslocal.exe"
        log.warning(msg)
        return TaskResult(code=ResultCode.VPN_NOT_RUNNING, message=msg)
