from clockin_bot.vpn.connect_ss_local import start_vpn
from clockin_bot.tools.retry_runner import run_with_retry
from clockin_bot.tools.log_utils import report_and_notify
from clockin_bot.clockin.base.result import TaskResult, ResultCode

def ensure_vpn_ready() -> TaskResult:
    """
    啟動 VPN，並進行最多 3 次重試。
    若成功則回傳 SUCCESS，否則會自動推播錯誤訊息與 log。
    """
    result = run_with_retry(start_vpn, retry=3, delay_sec=1)

    if result.code != ResultCode.SUCCESS:
        report_and_notify(result)

    return result
