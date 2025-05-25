import pytest
from unittest.mock import patch
from clockin_bot.tools import utils_delay

def test_get_random_delay_range():
    # 連跑 20 次，確認隨機值都在 60～480 秒之間
    for _ in range(20):
        delay = utils_delay.get_random_delay()
        assert 60 <= delay <= 480

def test_random_delay_behavior():
    # 模擬 get_random_delay 回傳固定秒數，並攔截 time.sleep
    with patch("clockin_bot.tools.utils_delay.get_random_delay", return_value=123) as mock_delay, \
         patch("clockin_bot.tools.utils_delay.time.sleep") as mock_sleep:
        utils_delay.random_delay()
        mock_delay.assert_called_once()
        mock_sleep.assert_called_once_with(123)
