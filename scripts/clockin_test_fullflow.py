from pathlib import Path
from vpn_outline_connect.connect_outline_vpn import connect_outline_vpn, disconnect_outline_vpn
from scripts.telegram_notify import send_telegram_message
from playwright.sync_api import sync_playwright

# === 旗標路徑設定 ===
BASE_DIR = Path(__file__).resolve().parent.parent
STORAGE_STATE_PATH = BASE_DIR / "data" / "login_state.json"

def clockin_test_fullflow():
    """模擬完整打卡流程（含VPN開啟連線，但不點打卡，只發TG訊息）"""

    print("🚀 啟動模擬打卡流程（包含VPN開啟）...")

    vpn_connected = connect_outline_vpn()

    if vpn_connected:
        print("✅ VPN連線成功，開始模擬打卡...")
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            context = browser.new_context(storage_state=str(STORAGE_STATE_PATH))
            page = context.new_page()

            page.goto("https://pro.104.com.tw/psc2?m=b&m=b,b,b")
            page.wait_for_load_state("networkidle")
            page.wait_for_timeout(3000)  # 等三秒讓網頁穩定

            # ⚠️ 不真的打卡，只是進頁面
            print("✅ 模擬打卡成功，發送TG通知...")
            send_telegram_message("✅ 測試模式：完整打卡流程模擬完成（未實際打卡）")

            browser.close()

        print("🛑 中斷VPN連線...")
        disconnect_outline_vpn()

    else:
        print("❌ VPN連線失敗，中止流程")
        send_telegram_message("❌ 測試模式：VPN連線失敗，中止打卡流程")

if __name__ == "__main__":
    clockin_test_fullflow()

