# utils_delay.py
import random
import time

def random_delay(min_minutes=1, max_minutes=8):
    """隨機延遲1～8分鐘（可以自訂範圍）"""
    delay_minutes = random.randint(min_minutes, max_minutes)
    print(f"⏳ 隨機延遲 {delay_minutes} 分鐘後繼續執行...")
    time.sleep(delay_minutes * 60)
