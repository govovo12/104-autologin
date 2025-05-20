from functools import wraps
from clockin_bot.logger.logger import get_logger  

log = get_logger("trace")

def log_call(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        log.info(f"開始呼叫函式：{func.__name__}")
        try:
            result = func(*args, **kwargs)
            log.info(f"函式結束執行：{func.__name__}")
            return result
        except Exception as e:
            log.error(f"函式執行錯誤：{func.__name__} - {e}")
            raise
    return wrapper

