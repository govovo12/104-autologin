import os
import time
import cv2
import numpy as np
import pyautogui
from pathlib import Path
from scripts.telegram_notify import send_telegram_message
from vpn_outline_connect.connect_outline_vpn import disconnect_outline_vpn  # ✅ 加這個！

# === 常數設定 ===
BASE_DIR = Path(__file__).resolve().parent.parent
IMAGE_DIR = BASE_DIR / "vpn_outline_connect"
OUTLINE_SHORTCUT_PATH = Path.home() / "Desktop" / "Outline.lnk"

# 圖片資源
CONNECT_BUTTON_IMG = IMAGE_DIR / "connect_button.png"
CONNECTED_TEXT_IMG = IMAGE_DIR / "connected_text.png"

# === 功能函式 ===

def launch_outline():
    """啟動 Outline 並將視窗移到前景"""
    os.startfile(OUTLINE_SHORTCUT_PATH)
    time.sleep(5)
    try:
        outline_window = pyautogui.getWindowsWithTitle("Outline")[0]
        if outline_window.isMinimized:
            outline_window.restore()
        outline_window.activate()
    except Exception as e:
        print(f"找不到 Outline 視窗: {e}")
        send_telegram_message("❌ 找不到 Outline 視窗，啟動失敗")
        return False
    return True

def match_template(target_img_path, threshold=0.8):
    """使用模板比對"""
    screen = pyautogui.screenshot()
    screen = cv2.cvtColor(np.array(screen), cv2.COLOR_RGB2BGR)
    template = cv2.imread(str(target_img_path))
    res = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, _ = cv2.minMaxLoc(res)
    return max_val >= threshold

def wait_for_image(target_img_path, timeout=10, threshold=0.8):
    """等待圖片出現"""
    start = time.time()
    while time.time() - start < timeout:
        if match_template(target_img_path, threshold):
            return True
        time.sleep(1)
    return False

def simple_connect_outline():
    """只負責打開Outline並確保連線，最後關掉"""
    if not launch_outline():
        return False

    if match_template(CONNECTED_TEXT_IMG):
        print("✅ Outline 已經連線")
    else:
        print("🔄 尚未連線，嘗試點擊連線按鈕...")

        if not wait_for_image(CONNECT_BUTTON_IMG, timeout=10):
            print("❌ 找不到連線按鈕")
            send_telegram_message("❌ 找不到連線按鈕，無法連線VPN")
            return False

        button_location = pyautogui.locateCenterOnScreen(str(CONNECT_BUTTON_IMG), confidence=0.8)
        if button_location:
            pyautogui.click(button_location)
            print("✅ 成功點擊連線按鈕")
        else:
            print("❌ 定位連線按鈕失敗")
            send_telegram_message("❌ 連線按鈕定位失敗")
            return False

        if wait_for_image(CONNECTED_TEXT_IMG, timeout=15):
            print("✅ VPN連線成功")
            send_telegram_message("✅ VPN連線成功（Check Cookie模式）")
        else:
            print("❌ VPN連線超時未成功")
            send_telegram_message("❌ VPN連線超時未成功（Check Cookie模式）")
            return False

    # ✅ 完成cookie檢查任務後，自動關掉Outline
    print("🛑 準備自動中斷連線並關閉Outline...")
    disconnect_outline_vpn()

    return True

if __name__ == "__main__":
    simple_connect_outline()

