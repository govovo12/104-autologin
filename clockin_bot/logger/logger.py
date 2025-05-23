import logging
from pathlib import Path
from datetime import datetime
import inspect


def get_logger(name: str = "clockin"):
    BASE_DIR = Path(__file__).resolve().parent.parent.parent
    LOG_DIR = BASE_DIR / "logs"
    LOG_DIR.mkdir(exist_ok=True)

    caller = inspect.stack()[1]
    print(f"[🪓 DEBUG] logger called from {caller.filename}:{caller.lineno}, writing to LOG_DIR = {LOG_DIR}")

    today_str = datetime.now().strftime("%Y-%m-%d")
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    if not logger.handlers:
        # 控制台輸出
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        ch.setFormatter(logging.Formatter("[%(levelname)s][%(name)s] %(message)s"))
        logger.addHandler(ch)

        # 每日 log：追加寫入
        daily_log_file = LOG_DIR / f"clockin_{today_str}.log"
        fh_daily = logging.FileHandler(daily_log_file, mode="a", encoding="utf-8")
        fh_daily.setLevel(logging.DEBUG)
        fh_daily.setFormatter(logging.Formatter("[%(asctime)s] %(message)s", "%Y-%m-%d %H:%M:%S"))
        logger.addHandler(fh_daily)

        # 最新 log：每次覆蓋
        latest_log_file = LOG_DIR / "latest_run.log"
        fh_latest = logging.FileHandler(latest_log_file, mode="w", encoding="utf-8")
        fh_latest.setLevel(logging.DEBUG)
        fh_latest.setFormatter(logging.Formatter("[%(asctime)s] %(message)s", "%Y-%m-%d %H:%M:%S"))
        logger.addHandler(fh_latest)

    return logger
