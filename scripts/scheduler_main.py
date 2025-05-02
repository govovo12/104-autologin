from vpn_outline_connect.connect_outline_vpn import connect_outline_vpn, disconnect_outline_vpn
from clockin_104.clockin_main import clockin_104
from utils_delay import random_delay
from utils_holiday import is_today_holiday
from telegram_notify import send_telegram_message

def main():
    if is_today_holiday():
        msg = "📅 今天是假日或手動排除日，自動跳過打卡流程"
        print(msg)
        send_telegram_message(msg)
        return

    # 智能啟動VPN
    vpn_connected = connect_outline_vpn()

    if vpn_connected:
        print("✅ VPN連線成功，準備隨機延後打卡...")
        random_delay()
        clockin_104()

        # 打卡後中斷VPN
        disconnected = disconnect_outline_vpn()
        if disconnected:
            send_telegram_message("✅ 打卡完成並成功斷開VPN")
        else:
            send_telegram_message("❌ 打卡後VPN中斷失敗，請手動檢查")

    else:
        print("❌ VPN連線失敗，停止後續打卡流程")
        send_telegram_message("❌ VPN連線失敗，已停止自動打卡流程")

if __name__ == "__main__":
    main()





