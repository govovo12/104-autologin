from pathlib import Path
import json
from datetime import datetime

# === 常數設定 ===
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
HOLIDAY_JSON = DATA_DIR / "holidays_2025.json"
MANUAL_SKIP_JSON = DATA_DIR / "manual_skip_days.json"

def is_today_holiday():
    """判斷今天是否國定假日或手動排除日"""
    today = datetime.today().strftime("%Y-%m-%d")

    try:
        with HOLIDAY_JSON.open("r", encoding="utf-8") as f:
            holidays = json.load(f)
    except Exception as e:
        print(f"讀取 holidays_2025.json 失敗: {e}")
        holidays = []

    try:
        with MANUAL_SKIP_JSON.open("r", encoding="utf-8") as f:
            manual_skips = json.load(f)
    except Exception as e:
        print(f"讀取 manual_skip_days.json 失敗: {e}")
        manual_skips = []

    return today in holidays or today in manual_skips


