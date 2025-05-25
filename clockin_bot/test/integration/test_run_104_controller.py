# test_run_104_controller.py
import pytest
from clockin_bot.vpn.connect_ss_local import start_vpn
from clockin_bot.clockin.controller.for_104_controller import run_clockin_104_flow
from clockin_bot.clockin.base.result import ResultCode
from clockin_bot.logger.safe_print import safe_print
@pytest.fixture(scope="session", autouse=True)
def ensure_vpn_connected():
    safe_print("🧪 [Fixture] 確保 Shadowsocks 已啟動...")
    result = start_vpn()
    assert result.code == ResultCode.SUCCESS, f"VPN 啟動失敗：{result.message}"

def test_run_104_controller_success():
    safe_print("🧪 [Test] 執行 104 打卡整合流程...")
    result = run_clockin_104_flow()
    assert result.code == ResultCode.SUCCESS, f"打卡失敗：{result.message}"
    assert "成功" in result.message or result.data, "打卡回傳內容異常"

