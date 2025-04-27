import time
import pyautogui
import pytesseract
import requests
import pygetwindow as gw
from PIL import ImageGrab
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID
from telegram_notify import send_telegram_message

# === Tesseract OCR 設定 ===
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# === 座標設定 ===
positions = {
    "connect_button_topleft": (1718, 811),
    "connect_button_bottomright": (1759, 836),
    "connected_topleft": (1594, 738),
    "connected_bottomright": (1645, 757),
}

# === 截圖指定範圍 ===
def capture_area(topleft, bottomright):
    return ImageGrab.grab(bbox=(topleft[0], topleft[1], bottomright[0], bottomright[1]))

# === OCR判斷連線成功 ===
def detect_connected():
    screenshot = capture_area(positions["connected_topleft"], positions["connected_bottomright"])
    text = pytesseract.image_to_string(screenshot, lang='eng+chi_tra')
    print(f"OCR偵測到的文字：{text.strip()}")
    return "已連線" in text

# === 等待 Outline 視窗出現 ===
def wait_for_outline_window(timeout=30):
    print("⌛ 等待 Outline 視窗啟動...")
    start_time = time.time()
    while time.time() - start_time < timeout:
        windows = gw.getWindowsWithTitle("Outline")
        if windows:
            print("🖥️ 找到 Outline 視窗！")
            return True
        time.sleep(1)
    print("❌ 找不到 Outline 視窗，可能啟動失敗")
    return False

# === 主控流程 ===
def connect_outline_vpn():
    print("🚀 Clockin-bot 主控流程啟動！（最終版）")
    print("🔍 檢查 Outline 狀態中...（由外部 .bat 啟動 Outline）")

    # 等待一點時間讓 Outline 真的打開
    time.sleep(8)

    # 新增：確認 Outline 視窗有打開
    if not wait_for_outline_window():
        send_telegram_message("❌ 無法啟動 Outline，停止後續打卡流程")
        return False

    max_retries = 3
    for attempt in range(1, max_retries + 1):
        print(f"🔎 第{attempt}次嘗試連線...")

        if detect_connected():
            print("🎯 VPN連線成功！")
            send_telegram_message("🎯 VPN連線成功！（Clockin-bot檢測）")
            return True

        print(f"⚠️ 第{attempt}次失敗，嘗試點擊連線按鈕...")

        # 點擊連線按鈕中心點
        center_x = (positions["connect_button_topleft"][0] + positions["connect_button_bottomright"][0]) // 2
        center_y = (positions["connect_button_topleft"][1] + positions["connect_button_bottomright"][1]) // 2
        pyautogui.click(center_x, center_y)
        time.sleep(5)

    print("❌ 三次都連線失敗")
    send_telegram_message("❌ VPN連線失敗，停止後續打卡流程")
    return False
