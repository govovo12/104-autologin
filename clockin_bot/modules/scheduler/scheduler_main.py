import sys
from datetime import datetime
from pathlib import Path
import shutil
from tools.env_loader import *

from clockin_bot.logger.logger import get_logger
from clockin_bot.notify.telegram_notify import send_telegram_message
from clockin_bot.vpn.connect_ss_local import start_vpn, is_vpn_connected
from clockin_bot.clockin.clockin_104 import clockin_104
from clockin_bot.tools.utils_delay import random_delay
from clockin_bot.tools.utils_holiday import is_today_holiday

log = get_logger("scheduler")

def copy_latest_log():
    base_dir = Path(__file__).resolve().parent.parent.parent
    log_dir = base_dir / "logs"
    today_str = datetime.now().strftime("%Y-%m-%d")
    src = log_dir / f"clockin_{today_str}.log"
    dst = log_dir / "latest_run.log"
    try:
        shutil.copy(src, dst)
    except Exception as e:
        log.warning(f"❌ 複製 latest_run.log 失敗：{e}")

def main():
    log.info("[1] Scheduler 主控流程啟動")
    log.info("[1] 開始執行 scheduler_main")

    if is_today_holiday():
        log.info("[2] 今天是休假日，停止執行打卡流程")
        send_telegram_message("⚠️ 今天是假日，系統停止打卡，不執行任何動作。")
        copy_latest_log()
        sys.exit(0)

    log.info("[3] 準備啟動 VPN（ss-local）")
    start_vpn()

    vpn_connected = is_vpn_connected()

    if vpn_connected:
        log.info("[4] VPN 啟動成功，開始打卡流程")
        clockin_success = clockin_104()
        log.info(f"[5] 打卡結果：{clockin_success}")

        if clockin_success:
            log.info("[6] 打卡成功")
        else:
            log.warning("[7] 打卡失敗，發送通知")
            send_telegram_message("⚠️ 打卡失敗，請檢查系統後續狀況。")
    else:
        log.error("[8] VPN 啟動失敗，系統終止打卡流程")
        send_telegram_message("❌ VPN 啟動失敗，打卡流程中止。")

    copy_latest_log()

if __name__ == "__main__":
    main()






    







