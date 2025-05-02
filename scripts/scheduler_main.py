# scripts/scheduler_main.py
from pathlib import Path
import sys

# === 旗標路徑設定（支援移動專案目錄）===
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR / "scripts"))
sys.path.append(str(BASE_DIR / "vpn_outline_connect"))

from connect_outline_vpn import connect_outline_vpn
from clockin_104 import clockin_104
from utils_delay import random_delay
from telegram_notify import send_telegram_message
from utils_holiday import is_today_holiday


def main():
    print("\U0001F680 Clockin-bot 主控流程啟動！")

    # ✅ 假日跳過機制
    if is_today_holiday():
        msg = "\U0001F6F8 今天是假日或手動請假，自動跳過打卡流程"
        print(msg)
        send_telegram_message(msg)
        return

    # ✅ 智能啟動 VPN
    vpn_connected = connect_outline_vpn()

    if vpn_connected:
        print("✅ VPN連線成功，準備隨機延遲後打卡...")
        random_delay()  # 延遲打卡，不延遲 VPN 啟動
        clockin_104()
    else:
        print("❌ VPN連線失敗，停止後續打卡流程")
        send_telegram_message("❌ VPN連線失敗，已停止自動打卡！")


if __name__ == "__main__":
    main()




