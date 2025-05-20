import subprocess
import time
import socket
import os


CONFIG_PATH = os.path.join(os.path.dirname(__file__), "ss_config.json")
SS_LOG_PATH = os.path.join(os.path.dirname(__file__), "ss.log")
LOCAL_SOCKS_PORT = 1080


def start_vpn():
    """啟動 ss-local 並建立 SOCKS5 代理連線"""
    # 若已有 ss-local 正在跑，先跳過（簡單 port check）
    if is_vpn_connected():
        print("[VPN] SOCKS5 proxy already running.")
        return

    print("[VPN] Starting ss-local...")
    command = [
        "nohup",
        "ss-local",
        "-c", CONFIG_PATH,
        "-v"
    ]
    with open(SS_LOG_PATH, "w") as log_file:
        subprocess.Popen(command, stdout=log_file, stderr=log_file)

    time.sleep(3)  # 等待 ss-local 啟動

    if is_vpn_connected():
        print("[VPN] SOCKS5 proxy started successfully.")
    else:
        print("[VPN] Failed to start ss-local. Check ss.log for details.")
        with open(SS_LOG_PATH, "r") as f:
            print(f.read())
        raise RuntimeError("VPN 啟動失敗")


def is_vpn_connected(host="127.0.0.1", port=LOCAL_SOCKS_PORT):
    """檢查 socks5 proxy 是否連得通"""
    try:
        with socket.create_connection((host, port), timeout=2):
            return True
    except Exception:
        return False


if __name__ == "__main__":
    start_vpn()
