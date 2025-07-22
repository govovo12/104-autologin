from clockin_bot.modules.scheduler.scheduler_utils import should_skip_today
from clockin_bot.vpn.vpn_controller import ensure_vpn_ready
from clockin_bot.clockin.controller.run_clockin_104_flow import run_clockin_104_flow
from clockin_bot.tools.retry_runner import run_with_retry
from clockin_bot.tools.log_utils import report_and_notify
from clockin_bot.tools.upload_log_to_pages import upload_log_only
from clockin_bot.clockin.base.result import ResultCode

# ✅ 開關：是否跳過假日判斷（True = 強制執行）
SKIP_HOLIDAY_CHECK = False


def run_scheduler():
    # Step 1: 檢查是否是假日或手動跳過
    if not SKIP_HOLIDAY_CHECK:
        result = should_skip_today()
        if result.code == ResultCode.SKIP_TODAY:
            report_and_notify(result)
            return  # 記得加 return 結束流程，避免後面繼續執行

    # Step 2: 啟動 VPN（內含 retry 與錯誤處理）
    vpn_result = ensure_vpn_ready()
    if vpn_result.code != ResultCode.SUCCESS:
        return

    # Step 3: 執行打卡流程（最多 retry 三次）
    result = run_with_retry(run_clockin_104_flow, retry=3, delay_sec=1)

    # Step 4: 回報結果（成功或失敗）
    report_and_notify(result)

    # ✅ Step 5: 自動上傳 log 報告到 GitHub Pages
    upload_log_only()


__task_info__ = {
    "name": "scheduler_main",
    "desc": "主流程：啟動 VPN → 執行打卡流程（含重試）→ 推播結果 + 上傳 log",
    "entry": run_scheduler,
}

if __name__ == "__main__":
    run_scheduler()
