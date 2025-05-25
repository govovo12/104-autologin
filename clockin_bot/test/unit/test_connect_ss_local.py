import pytest
from unittest.mock import patch, MagicMock
from pathlib import Path
from clockin_bot.vpn import connect_ss_local
from clockin_bot.clockin.base.result import ResultCode

@pytest.fixture
def mock_logger(monkeypatch):
    monkeypatch.setattr(connect_ss_local, "log", MagicMock())

def test_already_running(monkeypatch, mock_logger):
    monkeypatch.setattr(connect_ss_local, "is_port_open", lambda host, port: True)
    result = connect_ss_local.start_vpn()
    assert result.code == ResultCode.SUCCESS
    assert "already running" in result.message.lower()

def test_file_not_found(monkeypatch, mock_logger):
    monkeypatch.setattr(connect_ss_local, "is_port_open", lambda h, p: False)
    monkeypatch.setattr(connect_ss_local, "SSLOCAL_PATH", Path("not_exist.exe"))
    monkeypatch.setattr(connect_ss_local, "SS_CONFIG_PATH", Path("not_exist.json"))
    result = connect_ss_local.start_vpn()
    assert result.code == ResultCode.VPN_FILE_MISSING

def test_success_after_3s(monkeypatch, mock_logger):
    monkeypatch.setattr(connect_ss_local, "SSLOCAL_PATH", Path(__file__))
    monkeypatch.setattr(connect_ss_local, "SS_CONFIG_PATH", Path(__file__))

    call_count = {"i": 0}
    def fake_port_open(host, port):
        call_count["i"] += 1
        return call_count["i"] >= 3
    monkeypatch.setattr(connect_ss_local, "is_port_open", fake_port_open)

    mock_popen = MagicMock()
    monkeypatch.setattr(connect_ss_local.subprocess, "Popen", lambda *a, **kw: mock_popen)
    monkeypatch.setattr(connect_ss_local.time, "sleep", lambda x: None)

    result = connect_ss_local.start_vpn()
    assert result.code == ResultCode.SUCCESS
    assert "successfully" in result.message.lower()

def test_timeout_fail(monkeypatch, mock_logger):
    monkeypatch.setattr(connect_ss_local, "SSLOCAL_PATH", Path(__file__))
    monkeypatch.setattr(connect_ss_local, "SS_CONFIG_PATH", Path(__file__))
    monkeypatch.setattr(connect_ss_local, "is_port_open", lambda h, p: False)

    mock_popen = MagicMock()
    monkeypatch.setattr(connect_ss_local.subprocess, "Popen", lambda *a, **kw: mock_popen)
    monkeypatch.setattr(connect_ss_local.time, "sleep", lambda x: None)

    result = connect_ss_local.start_vpn()
    assert result.code == ResultCode.VPN_START_TIMEOUT
    assert "10 秒" in result.message or "10秒" in result.message

def test_subprocess_exception(monkeypatch, mock_logger):
    monkeypatch.setattr(connect_ss_local, "SSLOCAL_PATH", Path(__file__))
    monkeypatch.setattr(connect_ss_local, "SS_CONFIG_PATH", Path(__file__))
    monkeypatch.setattr(connect_ss_local, "is_port_open", lambda h, p: False)

    monkeypatch.setattr(
        connect_ss_local.subprocess,
        "Popen",
        lambda *a, **kw: (_ for _ in ()).throw(Exception("boom"))
    )
    result = connect_ss_local.start_vpn()
    assert result.code == ResultCode.VPN_START_EXCEPTION
    assert "boom" in result.message
