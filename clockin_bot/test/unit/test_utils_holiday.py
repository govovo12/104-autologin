import pytest
import json
import datetime
from unittest.mock import mock_open, patch
from clockin_bot.tools import utils_holiday
from pathlib import Path

@pytest.fixture
def mock_logger(monkeypatch):
    class FakeLogger:
        def info(self, *args, **kwargs): pass
        def error(self, *args, **kwargs): pass
    monkeypatch.setattr(utils_holiday, "log", FakeLogger())

def test_workday(monkeypatch, mock_logger):
    monkeypatch.setattr(utils_holiday, "HOLIDAY_JSON", Path("holiday.json"))
    monkeypatch.setattr(utils_holiday, "MANUAL_SKIP_JSON", Path("manual.json"))

    mock_data = json.dumps([
        {"西元日期": "20991231", "是否放假": "2"}
    ])

    with patch("pathlib.Path.open", mock_open(read_data=mock_data)):
        result = utils_holiday.is_today_holiday()
        assert result is False

def test_fixed_holiday(monkeypatch, mock_logger):
    monkeypatch.setattr(utils_holiday, "HOLIDAY_JSON", Path("holiday.json"))
    monkeypatch.setattr(utils_holiday, "MANUAL_SKIP_JSON", Path("manual.json"))

    today = datetime.datetime.today().strftime("%Y%m%d")
    holiday_data = json.dumps([
        {"西元日期": today, "是否放假": "2"}
    ])
    manual_data = json.dumps([])

    def fake_open(path, *args, **kwargs):
        if "holiday" in str(path):
            return mock_open(read_data=holiday_data)()
        else:
            return mock_open(read_data=manual_data)()

    with patch("pathlib.Path.open", fake_open):
        result = utils_holiday.is_today_holiday()
        assert result is True

def test_manual_skip(monkeypatch, mock_logger):
    monkeypatch.setattr(utils_holiday, "HOLIDAY_JSON", Path("holiday.json"))
    monkeypatch.setattr(utils_holiday, "MANUAL_SKIP_JSON", Path("manual.json"))

    today = datetime.datetime.today().strftime("%Y-%m-%d")
    holiday_data = json.dumps([])
    manual_data = json.dumps([today])

    def fake_open(path, *args, **kwargs):
        if "manual" in str(path):
            return mock_open(read_data=manual_data)()
        else:
            return mock_open(read_data=holiday_data)()

    with patch("pathlib.Path.open", fake_open):
        result = utils_holiday.is_today_holiday()
        assert result is True

def test_invalid_json(monkeypatch, mock_logger):
    monkeypatch.setattr(utils_holiday, "HOLIDAY_JSON", Path("holiday.json"))
    monkeypatch.setattr(utils_holiday, "MANUAL_SKIP_JSON", Path("manual.json"))

    def broken_open(path, *args, **kwargs):
        return mock_open(read_data="{ broken")()

    with patch("pathlib.Path.open", broken_open):
        result = utils_holiday.is_today_holiday()
        assert result is False
