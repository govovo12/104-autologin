import os
import random
import time

# 計算隨機延遲秒數（1~8 分鐘）
def get_random_delay():
    return random.randint(60, 480)  # 單位：秒

# 實作延遲邏輯
def random_delay():
    delay = get_random_delay()
    print(f"\u23f3 延遲 {delay} 秒後開始打卡...")
    time.sleep(delay)


# 如果你要單獨測試這支模組
if __name__ == "__main__":
    random_delay()
