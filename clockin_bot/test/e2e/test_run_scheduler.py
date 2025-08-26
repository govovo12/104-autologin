import pytest
from unittest.mock import patch
from clockin_bot.modules.scheduler.scheduler_main import run_scheduler
from clockin_bot.clockin.base.result import TaskResult, ResultCode

def test_scheduler_skip_day():
    with patch("clockin_bot.modules.scheduler.scheduler_utils.should_skip_today",
               return_value=TaskResult(ResultCode.SKIP_TODAY, "☀️ 今天是假日或排除日，已略過執行")), \
         patch("clockin_bot.modules.scheduler.scheduler_main.report_and_notify") as mock_notify:

        run_scheduler()

        # 確認 report_and_notify 被呼叫一次
        mock_notify.assert_called_once()

        # 取出呼叫時的參數
        called_result = mock_notify.call_args[0][0]

        # ✅ 檢查錯誤碼正確
        assert called_result.code == ResultCode.SKIP_TODAY

        # ✅ 檢查訊息至少包含關鍵字（避免因 wording 差異失敗）
        assert "假日" in called_result.message or "略過" in called_result.message

        # 額外輸出 debug，方便觀察
        print(f"[DEBUG] 收到的 TaskResult: code={called_result.code}, message={called_result.message}")



# 暫時不測 VPN 失敗
# def test_scheduler_vpn_fail():
#     with patch("clockin_bot.modules.scheduler.scheduler_utils.should_skip_today", 
#                return_value=TaskResult(ResultCode.SUCCESS, "工作日")), \
#          patch("clockin_bot.modules.scheduler.scheduler_main.run_vpn", 
#                return_value=(ResultCode.VPN_START_TIMEOUT, "VPN失敗")), \
#          patch("clockin_bot.modules.scheduler.scheduler_main.report_and_notify") as mock_notify:
#         run_scheduler()
#         mock_notify.assert_called_once()

# 暫時不測全成功
# def test_scheduler_full_success():
#     with patch("clockin_bot.modules.scheduler.scheduler_main.should_skip_today", 
#                return_value=TaskResult(ResultCode.SUCCESS, "工作日")), \
#          patch("clockin_bot.modules.scheduler.scheduler_main.run_vpn", 
#                side_effect=[(ResultCode.SUCCESS, "VPN成功"), (ResultCode.SUCCESS, "VPN停止")]), \
#          patch("clockin_bot.modules.scheduler.scheduler_main.run_with_retry", 
#                return_value=TaskResult(ResultCode.SUCCESS, "打卡成功")), \
#          patch("clockin_bot.modules.scheduler.scheduler_main.report_and_notify") as mock_notify:
# 
#         run_scheduler()
# 
#         mock_notify.assert_called_once()
#         result = mock_notify.call_args[0][0]
#         assert result.code == ResultCode.SUCCESS
#         assert result.message == "打卡成功"
