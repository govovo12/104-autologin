import json
from unittest.mock import patch
from datetime import datetime, timedelta
from pathlib import Path
import pytest

from clockin_bot.session import check_cookie_expiry_v2
from clockin_bot.clockin.base.result import ResultCode

@pytest.fixture
def fake_cookie_path(tmp_path, monkeypatch):
    # 攔截 COOKIE_FILE，改為 tmp_path 下的假檔案
    fake_path = tmp_path / "login_state.json"
    monkeypatch.setattr(check_cookie_expiry_v2, "COOKIE_FILE", fake_path)
    return fake_path

@pytest.fixture
def mock_telegram():
    # 攔截發送 Telegram 訊息
    with patch("clockin_bot.session.check_cookie_expiry_v2.send_telegram_message") as mock:
        yield mock

def write_cookie(file_path, cookies):
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump({"cookies": cookies}, f)

def test_file_not_exist(monkeypatch):
    monkeypatch.setattr(check_cookie_expiry_v2, "COOKIE_FILE", Path("non_existent.json"))
    with patch("clockin_bot.session.check_cookie_expiry_v2.send_telegram_message") as mock:
        result = check_cookie_expiry_v2.check_cookie_expiry()
        assert result.code == ResultCode.COOKIE_FILE_NOT_FOUND
        mock.assert_called_once()

def test_no_valid_cookie(fake_cookie_path, mock_telegram):
    write_cookie(fake_cookie_path, [{"name": "abc"}])
    result = check_cookie_expiry_v2.check_cookie_expiry()
    assert result.code == ResultCode.COOKIE_NO_VALID_EXPIRES
    mock_telegram.assert_called_once()

def test_expired_cookie(fake_cookie_path, mock_telegram):
    expired_ts = (datetime.now() - timedelta(days=1)).timestamp()
    write_cookie(fake_cookie_path, [{"name": "expired", "expires": expired_ts}])
    result = check_cookie_expiry_v2.check_cookie_expiry()
    assert result.code == ResultCode.COOKIE_ALREADY_EXPIRED
    mock_telegram.assert_called_once()

def test_cookie_near_expiry(fake_cookie_path, mock_telegram):
    near_expiry_ts = (datetime.now() + timedelta(days=3)).timestamp()
    write_cookie(fake_cookie_path, [{"name": "near", "expires": near_expiry_ts}])
    result = check_cookie_expiry_v2.check_cookie_expiry()
    assert result.code == ResultCode.SUCCESS
    mock_telegram.assert_called_once()

def test_cookie_not_expired(fake_cookie_path, mock_telegram):
    valid_ts = (datetime.now() + timedelta(days=10)).timestamp()
    write_cookie(fake_cookie_path, [{"name": "valid", "expires": valid_ts}])
    result = check_cookie_expiry_v2.check_cookie_expiry()
    assert result.code == ResultCode.SUCCESS
    mock_telegram.assert_called_once()

def test_json_parse_error(fake_cookie_path, mock_telegram):
    fake_cookie_path.write_text("{ broken json ")
    result = check_cookie_expiry_v2.check_cookie_expiry()
    assert result.code == ResultCode.COOKIE_PARSE_ERROR
    mock_telegram.assert_called_once()
