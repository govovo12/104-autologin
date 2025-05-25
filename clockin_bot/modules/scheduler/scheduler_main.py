from clockin_bot.modules.scheduler.scheduler_utils import should_skip_today
from clockin_bot.vpn.vpn_controller import ensure_vpn_ready
from clockin_bot.clockin.controller.for_104_controller import run_clockin_104_flow
from clockin_bot.tools.retry_runner import run_with_retry
from clockin_bot.tools.log_utils import report_and_notify
from clockin_bot.clockin.base.result import ResultCode

def run_scheduler():
    # Step 1: 檢查是否是假日或手動跳過
    #result = should_skip_today()
    #if result.code == ResultCode.SKIP_TODAY:
        #report_and_notify(result)
        #return

    # Step 2: 啟動 VPN（內含 retry 與錯誤處理）
    vpn_result = ensure_vpn_ready()
    if vpn_result.code != ResultCode.SUCCESS:
        return

    # Step 3: 執行打卡流程（最多 retry 三次）
    result = run_with_retry(run_clockin_104_flow, retry=3, delay_sec=1)

    # Step 4: 回報結果（成功或失敗）
    report_and_notify(result)

if __name__ == "__main__":
    run_scheduler()
from clockin_bot.modules.scheduler.scheduler_utils import should_skip_today
from clockin_bot.vpn.vpn_controller import ensure_vpn_ready
from clockin_bot.clockin.controller.for_104_controller import run_clockin_104_flow
from clockin_bot.tools.retry_runner import run_with_retry
from clockin_bot.tools.log_utils import report_and_notify
from clockin_bot.clockin.base.result import ResultCode

def run_scheduler():
    # Step 1: 檢查是否是假日或手動跳過
    # result = should_skip_today()
    # if result.code == ResultCode.SKIP_TODAY:
    #     report_and_notify(result)
    #     return

    # Step 2: 啟動 VPN（內含 retry 與錯誤處理）
    vpn_result = ensure_vpn_ready()
    if vpn_result.code != ResultCode.SUCCESS:
        return

    # Step 3: 執行打卡流程（最多 retry 三次）
    result = run_with_retry(run_clockin_104_flow, retry=3, delay_sec=1)

    # Step 4: 回報結果（成功或失敗）
    report_and_notify(result)

# ✅ 任務註冊
__task_info__ = {
    "name": "scheduler_main",
    "desc": "主流程：啟動 VPN → 執行打卡流程（含重試）→ 推播結果",
    "entry": run_scheduler,
}

if __name__ == "__main__":
    run_scheduler()
