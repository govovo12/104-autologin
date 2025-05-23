import subprocess
import time
import socket
import os

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

CONFIG_PATH = os.path.join(CURRENT_DIR, "ss_config.json")
LOCAL_SOCKS_PORT = 1080
SSLOCAL_PATH = os.path.abspath(
    os.path.join(CURRENT_DIR, "sslocal", "sslocal.exe")
)


def start_vpn():
    if is_vpn_connected():
        print("[VPN] SOCKS5 proxy already running.")
        return

    print("[VPN] Starting sslocal...")
    print(f"[VPN] 執行檔路徑: {SSLOCAL_PATH}")

    # 啟動 proxy，不阻塞主流程
    subprocess.Popen(
        [SSLOCAL_PATH, "-c", CONFIG_PATH, "-v"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    # 等待代理啟動
    time.sleep(1)

    if is_vpn_connected():
        print("[VPN] ✅ SOCKS5 proxy started successfully.")
    else:
        print("[VPN] ❌ Failed to start sslocal.")
        raise RuntimeError("VPN 啟動失敗")

def is_vpn_connected(host="127.0.0.1", port=LOCAL_SOCKS_PORT):
    try:
        with socket.create_connection((host, port), timeout=2):
            return True
    except Exception:
        return False

if __name__ == "__main__":
    start_vpn()

__task_info__ = {
    "name": "connect_ss_local",
    "desc": "啟動 Shadowsocks 本地代理（sslocal.exe）並驗證是否連線成功",
    "entry": start_vpn,
}
