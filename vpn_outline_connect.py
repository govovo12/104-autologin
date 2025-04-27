# vpn_outline_connect.py
import subprocess
import time
import pyautogui
import pytesseract
from PIL import ImageGrab
import pygetwindow as gw
from telegram_notify import send_telegram_message
from config import OUTLINE_PATH

# 設定tesseract路徑 【⚡這裡要填自己電腦的Tesseract安裝路徑】
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# 偏移參數（相對於Outline視窗左上角）
CONNECT_BTN_OFFSET_X = 300
CONNECT_BTN_OFFSET_Y = 497
CONNECTED_TEXT_BBOX = (146, 402, 217, 441)  # (左上x, 左上y, 右下x, 右下y)

def open_outline():
    subprocess.Popen(OUTLINE_PATH)
    print("✅ 已啟動 Outline，等待打開...")
    time.sleep(5)

def get_outline_window():
    return gw.getWindowsWithTitle('Outline')[0]

def get_connected_bbox():
    window = get_outline_window()
    return (
        window.left + CONNECTED_TEXT_BBOX[0],
        window.top + CONNECTED_TEXT_BBOX[1],
        window.left + CONNECTED_TEXT_BBOX[2],
        window.top + CONNECTED_TEXT_BBOX[3],
    )

def check_connected_ocr():
    bbox = get_connected_bbox()
    img = ImageGrab.grab(bbox=bbox)
    text = pytesseract.image_to_string(img, lang='chi_tra')
    print(f"OCR偵測到的文字：{text}")
    return "已連線" in text

def connect_outline_vpn():
    for attempt in range(3):
        try:
            print(f"🔎 第{attempt+1}次嘗試連線...")
            window = get_outline_window()
            connect_btn_x = window.left + CONNECT_BTN_OFFSET_X
            connect_btn_y = window.top + CONNECT_BTN_OFFSET_Y
            pyautogui.moveTo(connect_btn_x, connect_btn_y)
            time.sleep(2)
            pyautogui.click()
            print("✅ 已點擊連線按鈕，等待連線...")

            # OCR偵測10秒內是否成功
            connected = False
            for _ in range(10):
                if check_connected_ocr():
                    connected = True
                    break
                print("🔎 未偵測到連線，繼續檢查...")
                time.sleep(1)

            if connected:
                print("🎯 VPN連線成功！")
                send_telegram_message("✅ Outline VPN 連線成功！")
                return True
            else:
                raise Exception("OCR偵測10秒後仍未確認連線成功")

        except Exception as e:
            print(f"⚠️ 第{attempt+1}次失敗：{e}")
            if attempt == 2:
                print("❌ 三次都連線失敗")
                send_telegram_message("❌ Outline VPN 連線失敗！")
                return False
            else:
                time.sleep(3)

