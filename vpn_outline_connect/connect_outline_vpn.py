import os
import time
import cv2
import numpy as np
import pyautogui
from telegram_notify import send_telegram_message

# === 常數設定 ===
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTLINE_SHORTCUT_PATH = os.path.join(os.path.expanduser("~"), "Desktop", "Outline.lnk")
CONNECT_BUTTON_PATH = os.path.join(BASE_DIR, "connect_button.png")
CONNECTED_IMAGE_PATH = os.path.join(BASE_DIR, "connected_text.png")
DISCONNECT_BUTTON_PATH = os.path.join(BASE_DIR, "disconnect_button.png")
DISCONNECT_X_PATH = os.path.join(BASE_DIR, "disconnect_buttonx.png")

CONNECT_BUTTON_IMAGE = cv2.imread(CONNECT_BUTTON_PATH)
CONNECTED_IMAGE = cv2.imread(CONNECTED_IMAGE_PATH)
DISCONNECT_IMAGE = cv2.imread(DISCONNECT_BUTTON_PATH)
DISCONNECT_X_IMAGE = cv2.imread(DISCONNECT_X_PATH)

# === 圖像比對函式 ===
def match_template(screenshot, template, threshold=0.8):
    result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, _, max_loc = cv2.minMaxLoc(result)
    return max_val

def get_button_position(template, screenshot):
    result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
    _, _, _, max_loc = cv2.minMaxLoc(result)
    h, w = template.shape[:2]
    center_x = max_loc[0] + w // 2
    center_y = max_loc[1] + h // 2
    return center_x, center_y

def screenshot_outline():
    screenshot = pyautogui.screenshot()
    return cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

# === 主邏輯：可供 scheduler_main 使用 ===
def connect_outline_vpn():
    retry_count = 0
    max_retries = 3

    print("啟動 Outline...")
    os.startfile(OUTLINE_SHORTCUT_PATH)
    time.sleep(3)

    while retry_count < max_retries:
        print(f"第 {retry_count + 1} 次圖像分析中...")
        screenshot_np = screenshot_outline()
        filename = os.path.join(BASE_DIR, f"ocr_debug_{int(time.time())}.png")
        cv2.imwrite(filename, screenshot_np)
        print(f"已儲存截圖至 {filename}")

        if match_template(screenshot_np, CONNECTED_IMAGE) >= 0.95:
            print("已判斷為 [已連線]，穩定退出。")
            send_telegram_message("✅ VPN 連線成功")
            return True

        if match_template(screenshot_np, CONNECT_BUTTON_IMAGE) >= 0.95:
            x, y = get_button_position(CONNECT_BUTTON_IMAGE, screenshot_np)
            pyautogui.moveTo(x, y)
            pyautogui.click()
            print(f"找到 [連線] 按鈕，正在點擊 ({x}, {y})")
            print("點擊後等待 VPN 建立連線（延遲 5 秒）...")
            time.sleep(5)
        else:
            print("未找到 [連線] 按鈕，比對失敗，重試...")

        retry_count += 1

    print("❌ VPN 連線失敗，已重試 3 次")
    send_telegram_message("❌ VPN 連線失敗，請手動確認！")
    return False

# 如果你要單獨測試，也能跑
if __name__ == "__main__":
    connect_outline_vpn()
