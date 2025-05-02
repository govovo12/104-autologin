import os
import time
from pathlib import Path
from playwright.sync_api import sync_playwright
from telegram_notify import send_telegram_message

# 設定旗標路徑（相對於本檔案位置）
BASE_DIR = Path(__file__).resolve().parent.parent
STATE_PATH = BASE_DIR / "data" / "login_state.json"

# 自動打卡主邏輯
def clockin_104():
    print("\U0001F4C5 開始執行自動打卡流程...")
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(storage_state=str(STATE_PATH))
            page = context.new_page()
            page.goto("https://pro.104.com.tw/psc2/home")
            print("已開啟 104 打卡頁面，等待打卡按鈕出現...")
            page.wait_for_selector(".checkin-btn")
            time.sleep(1)

            # 判斷是否已打卡成功
            if page.query_selector(".text-success"):
                print("\u2705 已打卡成功，無需重複打卡。")
                send_telegram_message("\u2705 今日已打卡成功，無需重複執行。")
                browser.close()
                return

            # 尚未打卡，進行打卡動作
            for attempt in range(3):
                page.click(".checkin-btn")
                time.sleep(2)
                if page.query_selector(".text-success"):
                    print("\u2705 打卡成功！")
                    send_telegram_message("\u2705 打卡成功！")
                    break
                else:
                    print(f"第 {attempt + 1} 次打卡失敗，重試中...")
            else:
                print("\u274C 打卡失敗！")
                send_telegram_message("\u274C 打卡失敗，請手動確認狀態！")

            browser.close()
    except Exception as e:
        print(f"發生例外錯誤: {e}")
        send_telegram_message(f"\u26a0\ufe0f 打卡程序發生錯誤：{e}")
