import pytest
from unittest.mock import patch
from clockin_bot.notify.telegram_notify import send_telegram_message
from clockin_bot.config import config
from clockin_bot.clockin.base.result import ResultCode


@pytest.fixture(autouse=True)
def reset_config(monkeypatch):
    """測試前重設 TELEGRAM_TOKEN 與 CHAT_ID，避免污染測試"""
    monkeypatch.setattr(config, "TELEGRAM_BOT_TOKEN", "dummy_token")
    monkeypatch.setattr(config, "TELEGRAM_CHAT_ID", "dummy_chat_id")


def test_send_telegram_success():
    """測試成功發送 Telegram 推播"""
    class MockResponse:
        def raise_for_status(self): pass

    with patch("clockin_bot.notify.telegram_notify.requests.post", return_value=MockResponse()) as mock_post:
        result = send_telegram_message("測試訊息")
        mock_post.assert_called_once()
        assert result.code == ResultCode.SUCCESS
        assert "已推播" in result.message


def test_send_telegram_missing_token(monkeypatch):
    """測試未設定 TOKEN / CHAT_ID 時應跳過推播"""
    monkeypatch.setattr(config, "TELEGRAM_BOT_TOKEN", "")
    monkeypatch.setattr(config, "TELEGRAM_CHAT_ID", "")

    with patch("clockin_bot.notify.telegram_notify.requests.post") as mock_post:
        result = send_telegram_message("不應發送")
        mock_post.assert_not_called()
        assert result.code == ResultCode.NOTIFY_SKIP
        assert "略過" in result.message


def test_send_telegram_failure():
    """測試 Telegram 推播失敗時是否能回傳正確錯誤碼"""
    def raise_error(*args, **kwargs):
        raise Exception("Fake Error")

    with patch("clockin_bot.notify.telegram_notify.requests.post", side_effect=raise_error):
        result = send_telegram_message("會失敗的訊息")
        assert result.code == ResultCode.NOTIFY_FAILED
        assert "發送 Telegram 訊息失敗" in result.message
