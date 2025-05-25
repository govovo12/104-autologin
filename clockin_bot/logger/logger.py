import logging
from pathlib import Path
from datetime import datetime, date
import inspect
from clockin_bot.logger.safe_print import safe_print
def get_logger(name: str = "clockin"):
    BASE_DIR = Path(__file__).resolve().parent.parent.parent
    LOG_DIR = BASE_DIR / "logs"
    LOG_DIR.mkdir(exist_ok=True)

    today_str = date.today().isoformat()
    daily_log_file = LOG_DIR / f"clockin_{today_str}.log"

    # 🔥 刪除所有不是今天的 log（含 .backup、前幾天）
    for log_file in LOG_DIR.glob("clockin_*.log"):
        if log_file.name != f"clockin_{today_str}.log":
            try:
                log_file.unlink()
                safe_print(f"[🧹] 已刪除舊 log：{log_file.name}")
            except Exception as e:
                safe_print(f"[⚠️] 刪除失敗：{log_file.name} → {e}")

    # DEBUG：logger 建立位置
    caller = inspect.stack()[1]
    safe_print(f"[DEBUG] logger called from {caller.filename}:{caller.lineno}, writing to LOG_DIR = {LOG_DIR}")

    # 建立 logger 本體
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    if not logger.handlers:
        # Console log
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        ch.setFormatter(logging.Formatter("[%(levelname)s][%(name)s] %(message)s"))
        logger.addHandler(ch)

        # 每日 log（追加）
        fh_daily = logging.FileHandler(daily_log_file, mode="a", encoding="utf-8")
        fh_daily.setLevel(logging.DEBUG)
        fh_daily.setFormatter(logging.Formatter("[%(asctime)s] %(message)s", "%Y-%m-%d %H:%M:%S"))
        logger.addHandler(fh_daily)

        # latest_run.log（覆蓋）
        latest_log_file = LOG_DIR / "latest_run.log"
        fh_latest = logging.FileHandler(latest_log_file, mode="w", encoding="utf-8")
        fh_latest.setLevel(logging.DEBUG)
        fh_latest.setFormatter(logging.Formatter("[%(asctime)s] %(message)s", "%Y-%m-%d %H:%M:%S"))
        logger.addHandler(fh_latest)

    return logger
