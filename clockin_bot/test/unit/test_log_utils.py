import pytest
from unittest.mock import patch, MagicMock
from clockin_bot.tools.log_utils import report_and_notify
from clockin_bot.clockin.base.result import TaskResult, ResultCode

def test_report_and_notify_success():
    with patch("clockin_bot.tools.log_utils.log") as mock_log, \
         patch("clockin_bot.tools.log_utils.send_telegram_message") as mock_tg, \
         patch("clockin_bot.tools.log_utils.upload_log") as mock_upload:

        result = TaskResult(code=ResultCode.SUCCESS, message="打卡成功")
        report_and_notify(result)

        mock_log.info.assert_called_once_with("打卡成功")
        mock_tg.assert_called_once_with("✅ 打卡成功")
        mock_upload.assert_not_called()

def test_report_and_notify_failure():
    with patch("clockin_bot.tools.log_utils.log") as mock_log, \
         patch("clockin_bot.tools.log_utils.send_telegram_message") as mock_tg, \
         patch("clockin_bot.tools.log_utils.upload_log") as mock_upload:

        result = TaskResult(code=ResultCode.API_REQUEST_EXCEPTION, message="打卡失敗")
        report_and_notify(result)

        mock_log.error.assert_called_once_with("[API_REQUEST_EXCEPTION] 打卡失敗")
        mock_tg.assert_called_once_with("❌ [API_REQUEST_EXCEPTION] 打卡失敗")
        mock_upload.assert_called_once()
