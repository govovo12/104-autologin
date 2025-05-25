import pytest
from unittest.mock import patch
from clockin_bot.modules.scheduler.scheduler_main import run_scheduler
from clockin_bot.clockin.base.result import TaskResult, ResultCode

def test_scheduler_skip_day():
    # 今天是假日或手動排除
    with patch("clockin_bot.modules.scheduler.scheduler_utils.should_skip_today", return_value=TaskResult(ResultCode.SKIP_TODAY, "跳過")), \
         patch("clockin_bot.modules.scheduler.scheduler_main.report_and_notify") as mock_notify:
        run_scheduler()
        mock_notify.assert_called_once()

def test_scheduler_vpn_fail():
    # VPN 連線失敗
    with patch("clockin_bot.modules.scheduler.scheduler_utils.should_skip_today", return_value=TaskResult(ResultCode.SUCCESS, "工作日")), \
         patch("clockin_bot.vpn.vpn_controller.ensure_vpn_ready", return_value=TaskResult(ResultCode.VPN_START_TIMEOUT, "VPN失敗")), \
         patch("clockin_bot.modules.scheduler.scheduler_main.report_and_notify") as mock_notify:
        run_scheduler()
        mock_notify.assert_called_once()

def test_scheduler_full_success():
    with patch("clockin_bot.modules.scheduler.scheduler_main.should_skip_today", return_value=TaskResult(ResultCode.SUCCESS, "工作日")), \
         patch("clockin_bot.modules.scheduler.scheduler_main.ensure_vpn_ready", return_value=TaskResult(ResultCode.SUCCESS, "VPN成功")), \
         patch("clockin_bot.modules.scheduler.scheduler_main.run_with_retry", return_value=TaskResult(ResultCode.SUCCESS, "打卡成功")), \
         patch("clockin_bot.modules.scheduler.scheduler_main.report_and_notify") as mock_notify:

        run_scheduler()

        # 驗證通知確實被觸發，並且內容正確
        mock_notify.assert_called_once()
        result = mock_notify.call_args[0][0]
        assert result.code == ResultCode.SUCCESS
        assert result.message == "打卡成功"


