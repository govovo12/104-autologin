# scheduler_main.py
from vpn_outline_connect import connect_outline_vpn
from clockin_104 import clockin_104
from utils_delay import random_delay
from telegram_notify import send_telegram_message

def main():
    print("🚀 Clockin-bot 主控流程啟動！")
    
    vpn_connected = connect_outline_vpn()

    if vpn_connected:
        print("✅ VPN連線成功，準備隨機延遲後打卡...")
        random_delay()  # 這邊只延遲打卡，不延遲VPN
        clockin_104()
    else:
        print("❌ VPN連線失敗，停止後續打卡流程")
        send_telegram_message("❌ VPN連線失敗，已停止自動打卡！")

if __name__ == "__main__":
    main()

