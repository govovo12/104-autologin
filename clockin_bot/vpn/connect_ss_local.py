import subprocess
import time
import httpx
from pathlib import Path
from clockin_bot.clockin.base.result import TaskResult, ResultCode
from clockin_bot.logger.logger import get_logger

log = get_logger("vpn")

# ✅ 指向 clockin_bot/
BASE_DIR = Path(__file__).resolve().parent.parent
EXE_PATH = BASE_DIR / "vpn" / "sslocal" / "sslocal.exe"
CONFIG_PATH = BASE_DIR / "vpn" / "sslocal" / "ss_config.json"



def get_current_ip() -> str:
    try:
        proxies = {
            "http://": "socks5://127.0.0.1:1080",
            "https://": "socks5://127.0.0.1:1080",
        }
        response = httpx.get("https://api.ipify.org", proxies=proxies, timeout=5)
        return response.text
    except Exception:
        return "❌ 無法透過 VPN 查詢 IP"


def start_vpn() -> TaskResult:
    """
    啟動 Shadowsocks（sslocal.exe）。
    若成功則回傳 SUCCESS 並附帶出口 IP。
    """
    try:
        if not EXE_PATH.exists() or not CONFIG_PATH.exists():
            msg = f"❌ VPN 執行檔或設定檔遺失：{EXE_PATH} / {CONFIG_PATH}"
            log.error(msg)
            return TaskResult(code=ResultCode.VPN_FILE_MISSING, message=msg)

        # ✅ 執行 VPN
        process = subprocess.Popen(
            [str(EXE_PATH), "-c", str(CONFIG_PATH)],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        time.sleep(2)

        if process.poll() is not None:
            msg = "❌ VPN 啟動失敗，sslocal.exe 沒有成功執行"
            log.error(msg)
            return TaskResult(code=ResultCode.VPN_START_EXCEPTION, message=msg)

        ip = get_current_ip()
        msg = f"✅ VPN 啟動成功，出口 IP：{ip}"
        log.info(msg)
        return TaskResult(code=ResultCode.SUCCESS, message=msg, data={"ip": ip})

    except Exception as e:
        msg = f"❌ 啟動 VPN 發生例外：{e}"
        log.exception(msg)
        return TaskResult(code=ResultCode.VPN_START_EXCEPTION, message=msg)
