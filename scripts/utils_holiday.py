import json
from datetime import datetime
from pathlib import Path

# === 假日判定模組 ===
BASE_DIR = Path(__file__).resolve().parent.parent
HOLIDAY_JSON = BASE_DIR / "data" / "holidays_2025.json"
MANUAL_SKIP_JSON = BASE_DIR / "data" / "manual_skip_days.json"

def is_today_holiday():
    today = datetime.today().strftime("%Y-%m-%d")
    
    try:
        with open(HOLIDAY_JSON, "r", encoding="utf-8") as f:
            holidays = json.load(f)
    except Exception as e:
        print(f"[錯誤] 讀取 holidays_2025.json 失敗: {e}")
        holidays = []

    try:
        with open(MANUAL_SKIP_JSON, "r", encoding="utf-8") as f:
            manual_skips = json.load(f)
    except Exception as e:
        print(f"[錯誤] 讀取 manual_skip_days.json 失敗: {e}")
        manual_skips = []

    return today in holidays or today in manual_skips

