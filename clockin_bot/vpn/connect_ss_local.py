import os
import subprocess
import time
import socket
from pathlib import Path
from clockin_bot.logger.logger import get_logger
from clockin_bot.logger.decorators import log_call
from clockin_bot.clockin.base.result import TaskResult, ResultCode

log = get_logger("vpn")

SSLOCAL_PATH = Path(__file__).resolve().parent / "sslocal" / "sslocal.exe"
SS_CONFIG_PATH = Path(__file__).resolve().parent / "sslocal" / "ss_config.json"

def is_port_open(host: str, port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(2)
        return sock.connect_ex((host, port)) == 0

@log_call
def start_vpn() -> TaskResult:
    if is_port_open("127.0.0.1", 1080):
        msg = "SOCKS5 proxy already running."
        log.info(msg)
        return TaskResult(code=ResultCode.SUCCESS, message=msg)

    if not SSLOCAL_PATH.exists() or not SS_CONFIG_PATH.exists():
        msg = "sslocal.exe 或 ss_config.json 不存在"
        log.error(msg)
        return TaskResult(code=ResultCode.VPN_FILE_MISSING, message=msg)

    try:
        subprocess.Popen(
            [str(SSLOCAL_PATH), "-c", str(SS_CONFIG_PATH)],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            creationflags=subprocess.CREATE_NO_WINDOW
        )

        for i in range(10):
            time.sleep(1)
            if is_port_open("127.0.0.1", 1080):
                msg = f"SOCKS5 proxy started successfully after {i + 1} sec."
                log.info(msg)
                return TaskResult(code=ResultCode.SUCCESS, message=msg)

        msg = "VPN 啟動後 10 秒仍無法連線"
        log.error(msg)
        return TaskResult(code=ResultCode.VPN_START_TIMEOUT, message=msg)

    except Exception as e:
        msg = f"啟動 sslocal 發生例外：{e}"
        log.error(msg)
        return TaskResult(code=ResultCode.VPN_START_EXCEPTION, message=msg)

__task_info__ = {
    "name": "connect_ss_local",
    "desc": "啟動 Shadowsocks 本地代理（sslocal.exe）並驗證是否連線成功",
    "entry": start_vpn
}
