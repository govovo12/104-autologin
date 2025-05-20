from pathlib import Path
import json
from datetime import datetime
from clockin_bot.logger.logger import get_logger
from clockin_bot.logger.decorators import log_call

log = get_logger("holiday")

# === 常數設定 ===
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
HOLIDAY_JSON = DATA_DIR / "holidays_2025.json"
MANUAL_SKIP_JSON = DATA_DIR / "manual_skip_days.json"

@log_call
def is_today_holiday():
    """判斷今天是否為固定假日或手動跳過日"""
    today_str = datetime.today().strftime("%Y%m%d")
    today_dash_str = datetime.today().strftime("%Y-%m-%d")
    log.info(f"開始檢查日期：{today_str} / {today_dash_str}")

    try:
        with HOLIDAY_JSON.open("r", encoding="utf-8") as f:
            holidays = json.load(f)
        log.info(f"成功讀取 holidays_2025.json，共 {len(holidays)} 筆資料")
    except Exception as e:
        log.error(f"讀取 holidays_2025.json 失敗: {e}")
        holidays = []

    try:
        with MANUAL_SKIP_JSON.open("r", encoding="utf-8") as f:
            manual_skips = json.load(f)
        log.info(f"成功讀取 manual_skip_days.json，共 {len(manual_skips)} 筆資料")
    except Exception as e:
        log.error(f"讀取 manual_skip_days.json 失敗: {e}")
        manual_skips = []

    for day in holidays:
        if day.get("西元日期") == today_str and day.get("是否放假") == "2":
            log.info("今天是固定假日，停止執行")
            return True

    if today_dash_str in manual_skips:
        log.info("今天為手動設定跳過日，停止執行")
        return True

    log.info("今天是工作日，繼續執行")
    return False




