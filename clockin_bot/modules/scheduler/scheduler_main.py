import sys
from clockin_bot.logger.logger import get_logger
from clockin_bot.logger.decorators import log_call
from clockin_bot.vpn.connect_ss_local import start_vpn, is_vpn_connected
from clockin_bot.clockin.clockin_104 import clockin_104
from clockin_bot.session.check_cookie_expiry_v2 import check_cookie_expiry
from clockin_bot.tools.utils_holiday import is_today_holiday
from clockin_bot.tools.utils_delay import random_delay
from clockin_bot.tools.view_latest_log import view_latest_log_html
from clockin_bot.tools.upload_log_to_pages import upload_log_only
from clockin_bot.notify.telegram_notify import send_telegram_message

log = get_logger("scheduler")

@log_call
def main():
    log.info("[1] 開始執行 scheduler_main")

    if is_today_holiday():
        log.info("[2] 今天是假日或排除日，結束流程")
        return

    log.info("[3] 準備啟動 VPN（ss-local）")
    start_vpn()

    if not is_vpn_connected():
        log.error("[4] VPN 未成功啟動，結束流程")
        send_telegram_message("❌ VPN 啟動確認失敗，系統結束流程。")
        return

    log.info("[5] VPN 啟動成功，準備執行打卡流程（含重試機制）")
    send_telegram_message("✅ VPN 已啟動並成功連線，準備開始打卡流程")

    #random_delay()

    MAX_RETRY = 3
    clockin_success = False
    for attempt in range(1, MAX_RETRY + 1):
        log.info(f"[5-R{attempt}] 執行打卡流程（第 {attempt} 次嘗試）")
        if clockin_104():
            clockin_success = True
            log.info(f"[6] 打卡成功（第 {attempt} 次）")
            send_telegram_message(f"✅ 打卡成功（第 {attempt} 次）")
            break

    if not clockin_success:
        log.error("[6] 多次打卡仍失敗，結束流程")
        send_telegram_message("❌ 打卡流程失敗，請查閱 log")

    # ⬇️ 最後流程：產生報告、上傳
    view_latest_log_html()
    upload_log_only()

__task_info__ = {
    "name": "scheduler_main",
    "desc": "主控流程：假日排除 → 啟動 VPN → 執行打卡（含 retry） → 發送通知",
    "entry": main,
}


