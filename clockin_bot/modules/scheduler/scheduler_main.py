from clockin_bot.modules.scheduler.scheduler_utils import should_skip_today
from clockin_bot.vpn.vpn_controller import run_vpn
from clockin_bot.clockin.controller.run_clockin_104_flow import run_clockin_104_flow
from clockin_bot.tools.retry_runner import run_with_retry
from clockin_bot.tools.log_utils import report_and_notify
from clockin_bot.tools.upload_log_to_pages import upload_log_only
from clockin_bot.clockin.base.result import ResultCode
from clockin_bot.tools.printer.log_helper import log_code_message

# ✅ 開關：是否跳過假日判斷（True = 強制執行）
SKIP_HOLIDAY_CHECK = False


def run_scheduler():
    print("[DEBUG] 進入 run_scheduler()")

    # Step 1: 判斷是否跳過
    if not SKIP_HOLIDAY_CHECK:
        print("[DEBUG] 準備檢查是否跳過今天")
        result = should_skip_today()
        print(f"[DEBUG] should_skip_today() 結果: code={result.code}, raw={result}")
        if result.code == ResultCode.SKIP_TODAY:
            print("[DEBUG] 今天是假日或手動跳過，結束流程")
            report_and_notify(result)
            return

    # Step 2: 啟動 VPN
    print("[DEBUG] 準備啟動 VPN")
    rc, detail = run_vpn("start")
    print(f"[DEBUG] run_vpn 執行完畢, rc={rc}, detail={detail}")
    log_code_message(rc)   # ✅ 只傳 rc，不會再爆
    if ResultCode(rc) != ResultCode.SUCCESS:   # 強制轉成 Enum 比較
        print("[DEBUG] VPN 啟動失敗，中斷流程")
        return

    # Step 3: 執行打卡流程
    print("[DEBUG] 準備進入 run_clockin_104_flow")
    result = run_with_retry(run_clockin_104_flow, retry=3, delay_sec=1)
    print(f"[DEBUG] run_clockin_104_flow 執行完畢, result={result}")

    # Step 4: 關閉 VPN
    print("[DEBUG] 準備關閉 VPN")
    run_vpn("stop")
    print("[DEBUG] VPN 已關閉")

    # Step 5: 報告 & 上傳 log
    print("[DEBUG] 準備推播結果")
    report_and_notify(result)
    print("[DEBUG] 準備上傳 log")
    upload_log_only()
    print("[DEBUG] 上傳 log 完成")

    print("[DEBUG] run_scheduler() 結束")
    return ResultCode.SUCCESS, result





__task_info__ = {
    "name": "scheduler_main",
    "desc": "主流程：啟動 VPN → 執行打卡流程（含重試）→ 推播結果 + 上傳 log",
    "entry": run_scheduler,
}

if __name__ == "__main__":
    run_scheduler()
