import os
import random
import time
from clockin_bot.logger.logger import get_logger
from clockin_bot.logger.decorators import log_call

log = get_logger("delay")

@log_call
def get_random_delay():
    return random.randint(60, 480)  # 單位：秒

@log_call
def random_delay():
    delay = get_random_delay()
    log.info(f"隨機延遲 {delay} 秒後開始打卡...")
    time.sleep(delay)

if __name__ == "__main__":
    random_delay()

