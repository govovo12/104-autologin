import os
import time
import cv2
import numpy as np
import pyautogui
from pathlib import Path
from telegram_notify import send_telegram_message

# === 常數設定 ===
BASE_DIR = Path(__file__).resolve().parent.parent
IMAGE_DIR = BASE_DIR / "vpn_outline_connect"
OUTLINE_SHORTCUT_PATH = Path.home() / "Desktop" / "Outline.lnk"

# VPN 圖片路徑
CONNECT_BUTTON_IMG = IMAGE_DIR / "connect_button.png"
CONNECTED_TEXT_IMG = IMAGE_DIR / "connected_text.png"
DISCONNECT_BUTTON_IMG = IMAGE_DIR / "disconnect_button.png"
DISCONNECT_BUTTONX_IMG = IMAGE_DIR / "disconnect_buttonx.png"

# === 功能函式 ===

def launch_outline():
    """啟動 Outline 並將視窗移到前景"""
    os.startfile(OUTLINE_SHORTCUT_PATH)
    time.sleep(5)  # 等待程式啟動
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
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    return max_val >= threshold

def wait_for_image(target_img_path, timeout=10, threshold=0.8):
    """等待指定圖片出現"""
    start = time.time()
    while time.time() - start < timeout:
        if match_template(target_img_path, threshold):
            return True
        time.sleep(1)
    return False

def connect_outline_vpn():
    """智能連線 Outline"""
    if not launch_outline():
        return False

    # 啟動後，先檢查是否已連線
    if match_template(CONNECTED_TEXT_IMG):
        print("✅ 已連線狀態，跳過連線步驟")
        return True  # 直接回傳連線成功

    # 沒有已連線 → 去點連線按鈕
    print("🔄 尚未連線，嘗試點擊連線按鈕")
    if not wait_for_image(CONNECT_BUTTON_IMG, timeout=10):
        print("❌ 找不到連線按鈕")
        send_telegram_message("❌ 找不到連線按鈕，無法連線VPN")
        return False

    button_location = pyautogui.locateCenterOnScreen(str(CONNECT_BUTTON_IMG), confidence=0.8)
    if button_location:
        pyautogui.click(button_location)
        print("✅ 成功點擊連線按鈕")
    else:
        print("❌ 連線按鈕定位失敗")
        send_telegram_message("❌ 連線按鈕定位失敗")
        return False

    # 點了連線後，確認是否真的連線成功
    if wait_for_image(CONNECTED_TEXT_IMG, timeout=15):
        print("✅ VPN連線成功")
        return True
    else:
        print("❌ VPN連線超時未成功")
        send_telegram_message("❌ VPN連線超時未成功")
        return False

def disconnect_outline_vpn():
    """打卡完成後，中斷連線並關閉 Outline"""
    print("🛑 準備中斷連線...")

    if not wait_for_image(DISCONNECT_BUTTON_IMG, timeout=10):
        print("❌ 找不到中斷連線按鈕")
        send_telegram_message("❌ 找不到中斷連線按鈕")
        return False

    disconnect_location = pyautogui.locateCenterOnScreen(str(DISCONNECT_BUTTON_IMG), confidence=0.8)
    if disconnect_location:
        pyautogui.click(disconnect_location)
        print("✅ 點擊中斷連線按鈕")
    else:
        print("❌ 中斷連線按鈕定位失敗")
        send_telegram_message("❌ 中斷連線按鈕定位失敗")
        return False

    # 等待已中斷連線確認
    if not wait_for_image(DISCONNECT_BUTTONX_IMG, timeout=15):
        print("❌ 中斷連線超時未成功")
        send_telegram_message("❌ 中斷連線超時未成功")
        return False

    # 成功看到中斷連線，點右上角X關閉Outline
    try:
        outline_window = pyautogui.getWindowsWithTitle("Outline")[0]
        outline_window.close()
        print("✅ 成功關閉 Outline")
    except Exception as e:
        print(f"❌ 關閉 Outline 視窗失敗: {e}")
        send_telegram_message(f"❌ 關閉 Outline 視窗失敗: {e}")
        return False

    return True
