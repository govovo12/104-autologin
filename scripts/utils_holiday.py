from pathlib import Path
import json
from datetime import datetime

# === 常數設定 ===
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
HOLIDAY_JSON = DATA_DIR / "holidays_2025.json"
MANUAL_SKIP_JSON = DATA_DIR / "manual_skip_days.json"

def is_today_holiday():
    """判斷今天是否為國定假日或手動排除日"""
    today_str = datetime.today().strftime("%Y%m%d")  # 注意這裡！必須是8碼無破折號
    today_dash_str = datetime.today().strftime("%Y-%m-%d")  # 給 manual_skip_days 用

    # 讀取 holidays_2025.json
    try:
        with HOLIDAY_JSON.open("r", encoding="utf-8") as f:
            holidays = json.load(f)
    except Exception as e:
        print(f"讀取 holidays_2025.json 失敗: {e}")
        holidays = []

    # 讀取 manual_skip_days.json
    try:
        with MANUAL_SKIP_JSON.open("r", encoding="utf-8") as f:
            manual_skips = json.load(f)
    except Exception as e:
        print(f"讀取 manual_skip_days.json 失敗: {e}")
        manual_skips = []

    # 查詢今天是不是行政院公告假日（是否放假=2）
    for day in holidays:
        if day.get("西元日期") == today_str and day.get("是否放假") == "2":
            return True

    # 查詢今天是不是自己手動排除的日子
    if today_dash_str in manual_skips:
        return True

    return False



