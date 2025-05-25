import pytest
from unittest.mock import patch, mock_open
from clockin_bot.modules.scheduler.scheduler_utils import should_skip_today
from clockin_bot.clockin.base.result import ResultCode

@pytest.fixture
def mock_logger(monkeypatch):
    class FakeLogger:
        def info(self, *args, **kwargs): pass
        def error(self, *args, **kwargs): pass
    monkeypatch.setattr("clockin_bot.modules.scheduler.scheduler_utils.log", FakeLogger())

def test_should_skip_today_on_holiday(monkeypatch, mock_logger):
    # 模擬今天是假日或手動排除日
    monkeypatch.setattr("clockin_bot.modules.scheduler.scheduler_utils.is_today_holiday", lambda: True)
    result = should_skip_today()
    assert result.code == ResultCode.SKIP_TODAY
    assert "假日" in result.message

def test_should_skip_today_on_workday(monkeypatch, mock_logger):
    # 模擬今天是工作日
    monkeypatch.setattr("clockin_bot.modules.scheduler.scheduler_utils.is_today_holiday", lambda: False)
    result = should_skip_today()
    assert result.code == ResultCode.SUCCESS
    assert "工作日" in result.message

def test_should_skip_today_exception(monkeypatch, mock_logger):
    # 模擬 is_today_holiday() 發生例外
    def raise_error():
        raise ValueError("假錯誤")
    monkeypatch.setattr("clockin_bot.modules.scheduler.scheduler_utils.is_today_holiday", raise_error)
    result = should_skip_today()
    assert result.code == ResultCode.UNKNOWN_ERROR
    assert "錯誤" in result.message
