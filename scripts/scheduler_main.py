from vpn_outline_connect.connect_outline_vpn import connect_outline_vpn, disconnect_outline_vpn
from scripts.clockin_104 import clockin_104
from scripts.utils_delay import random_delay
from scripts.utils_holiday import is_today_holiday
from scripts.telegram_notify import send_telegram_message

# === 主控制流程 ===
if __name__ == "__main__":
    if is_today_holiday():
         print("🚫 今天是週六日、行政院假日或自訂請假日，不執行打卡流程")
         send_telegram_message("🚫 今天是假日或排除日，不執行打卡！")
         exit()

    vpn_connected = connect_outline_vpn()   # ✅ 必須判斷 VPN 有成功連上！

    if vpn_connected:
        #random_delay()  # ✅ 隨機延遲
        clockin_success = clockin_104()  # ✅ 執行打卡

        if clockin_success:
            disconnect_outline_vpn()
        else:
            send_telegram_message("⚠️ 打卡失敗，中斷後續流程！")
            disconnect_outline_vpn()
    else:
        send_telegram_message("❌ VPN連線失敗，停止自動打卡流程")




    







