import subprocess
import time
import pyautogui
import pytesseract
import requests
import pygetwindow as gw
from PIL import ImageGrab

# === Telegram Bot 資訊 ===
TELEGRAM_BOT_TOKEN = '7880668864:AAGaji_gX7WJMifuQIXRtcX-vlbGF6Z2ZEc'
TELEGRAM_CHAT_ID = '6184827725'

# === Outline 路徑設定 ===
OUTLINE_PATH = r"C:\Program Files (x86)\Outline\Outline.exe"

# === Tesseract OCR 設定 ===
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message
    }
    try:
        response = requests.post(url, data=payload)
        response.raise_for_status()
        print("📬 成功發送Telegram訊息")
    except Exception as e:
        print(f"⚠️ 發送Telegram失敗：{e}")

def open_outline():
    subprocess.Popen(OUTLINE_PATH)
    print("✅ 已啟動 Outline，等待打開...")
    time.sleep(5)  # 等待Outline啟動完成

def get_outline_window():
    return gw.getWindowsWithTitle('Outline')[0]

def get_connected_bbox():
    outline_window = get_outline_window()
    window_left = outline_window.left
    window_top = outline_window.top

    # 調整過，放大OCR範圍
    x1 = window_left + 146
    y1 = window_top + 402
    x2 = window_left + 217
    y2 = window_top + 441
    return (x1, y1, x2, y2)


def check_connected_ocr():
    bbox = get_connected_bbox()
    img = ImageGrab.grab(bbox=bbox)

    text = pytesseract.image_to_string(img, lang='chi_tra')
    print(f"OCR偵測到的文字：{text}")

    if "已連線" in text:
        print("✅ 偵測到已連線成功！")
        return True
    else:
        print("❌ 沒偵測到連線成功")
        return False

def connect_vpn():
    for attempt in range(3):
        try:
            print(f"🔎 第{attempt+1}次嘗試連線...")

            outline_window = get_outline_window()
            window_left = outline_window.left
            window_top = outline_window.top

            # 點擊連線按鈕中心點
            connect_btn_x = window_left + 300
            connect_btn_y = window_top + 497

            pyautogui.moveTo(connect_btn_x, connect_btn_y)
            print(f"⏳ 移動到連線按鈕中心 ({connect_btn_x}, {connect_btn_y})，準備點擊...（2秒後）")
            time.sleep(2)
            pyautogui.click()
            print("✅ 已點擊連線按鈕，等待連線...")
            time.sleep(5)

            print("⏳ 開始OCR連續偵測（最多10秒）...")
            connected = False
            for i in range(10):
                if check_connected_ocr():
                    connected = True
                    break
                else:
                    print(f"🔎 第{i+1}秒：未偵測到，繼續偵測...")
                    time.sleep(1)

            if connected:
                print("🎯 VPN連線成功！（連續偵測確認）")
                send_telegram_message("✅ Outline VPN 連線成功！")
                return True
            else:
                raise Exception("連續偵測10秒後仍未確認連線成功")

        except Exception as e:
            print(f"⚠️ 第{attempt+1}次失敗：{e}")
            if attempt == 2:
                print("❌ 三次都連線失敗")
                send_telegram_message("❌ Outline VPN 連線失敗！")
                return False
            else:
                print("⏳ 重試中...")
                time.sleep(3)

if __name__ == "__main__":
    open_outline()
    connect_vpn()

