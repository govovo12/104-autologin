import pytest
from unittest.mock import patch, MagicMock
from clockin_bot.vpn.vpn_controller import ensure_vpn_ready
from clockin_bot.clockin.base.result import TaskResult, ResultCode

def test_vpn_success():
    # 模擬 start_vpn 成功
    with patch("clockin_bot.vpn.vpn_controller.start_vpn", return_value=TaskResult(code=ResultCode.SUCCESS, message="OK")), \
         patch("clockin_bot.vpn.vpn_controller.report_and_notify") as mock_notify:

        result = ensure_vpn_ready()
        assert result.code == ResultCode.SUCCESS
        mock_notify.assert_not_called()

def test_vpn_fail_after_retries():
    # 模擬 start_vpn 永遠失敗
    fail_result = TaskResult(code=ResultCode.VPN_START_TIMEOUT, message="VPN 一直沒通")
    with patch("clockin_bot.vpn.vpn_controller.start_vpn", return_value=fail_result), \
         patch("clockin_bot.vpn.vpn_controller.report_and_notify") as mock_notify:

        result = ensure_vpn_ready()
        assert result.code == ResultCode.VPN_START_TIMEOUT
        mock_notify.assert_called_once_with(fail_result)
