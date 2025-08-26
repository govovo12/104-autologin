# clockin_bot/vpn/vpn_operator.py

import subprocess
import time
import psutil
import json
from pathlib import Path
from clockin_bot.tools.common.result_code import ResultCode
import requests

# 🔧 Debug 開關
DEBUG = False

# 🔧 保存全域 process，避免被 GC
_vpn_process = None


def _log_debug(msg):
    """只在 DEBUG=True 時輸出訊息"""
    if DEBUG:
        print(f"[DEBUG][vpn_operator] {msg}")


def _load_vpn_config(config_path: Path):
    """讀取 JSON 設定檔"""
    if not config_path.exists():
        return ResultCode.TASK_VPN_CONFIG_FILE_NOT_FOUND, None

    try:
        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)
    except Exception as e:
        _log_debug(f"載入設定檔失敗: {e}")
        return ResultCode.TASK_VPN_CONFIG_INVALID_FORMAT, None

    if "exe_path" not in config or "params" not in config:
        _log_debug("設定檔缺少 exe_path 或 params")
        return ResultCode.TASK_VPN_CONFIG_INVALID_FORMAT, None

    return ResultCode.SUCCESS, config


def _is_tun2socks_running():
    """檢查 tun2socks 進程是否已存在"""
    for proc in psutil.process_iter(["pid", "name", "cmdline"]):
        cmdline = proc.info["cmdline"] or []
        if cmdline and "tun2socks" in " ".join(cmdline).lower():
            return proc.pid
    return None


def _is_route_exist(target: str) -> bool:
    """檢查指定路由是否已存在"""
    route_result = subprocess.run(["route", "print"], capture_output=True, text=True)
    return target in route_result.stdout


def start_vpn(config_path: Path, interface_name: str, skip_ip_check: bool):
    """啟動 VPN（tun2socks）並設定全域路由"""
    global _vpn_process

    existing_pid = _is_tun2socks_running()
    if existing_pid:
        return ResultCode.SUCCESS, {
            "pid": existing_pid,
            "note": "VPN 已經在運行，略過啟動",
            "interface_name": interface_name,
            "skip_ip_check": skip_ip_check
        }

    rc, config = _load_vpn_config(config_path)
    if rc != ResultCode.SUCCESS:
        return rc, None

    exe_path = config["exe_path"]
    params = config["params"]
    _log_debug(f"準備啟動 tun2socks: {exe_path}")
    _log_debug(f"參數: {params}")

    try:
        if DEBUG:
            _vpn_process = subprocess.Popen(
                [exe_path] + params,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
        else:
            _vpn_process = subprocess.Popen(
                [exe_path] + params,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
    except Exception as e:
        _log_debug(f"Popen 失敗: {e}")
        print(f"[VPN] 無法啟動 tun2socks: {e}")
        return ResultCode.TASK_VPN_START_TIMEOUT, None

    # 偵測 tun2socks PID
    tun2socks_pid = None
    start_time = time.time()

    while True:
        if time.time() - start_time > 15:
            print("[VPN] 15 秒內未找到 tun2socks 進程")
            return ResultCode.TASK_VPN_PROCESS_NOT_FOUND, None

        for proc in psutil.process_iter(["pid", "name", "cmdline"]):
            cmdline = proc.info["cmdline"] or []
            if cmdline and "tun2socks" in " ".join(cmdline).lower():
                tun2socks_pid = proc.pid
                break
        if tun2socks_pid:
            break
        time.sleep(0.5)

    try:
        tun_gw = params[params.index("-tunGw") + 1]
    except ValueError:
        print("[VPN] 缺少 -tunGw 參數")
        return ResultCode.TASK_VPN_TUN_GW_MISSING, None

    if not _is_route_exist(tun_gw):
        try:
            result1 = subprocess.run(
                ["route", "add", "0.0.0.0", "mask", "128.0.0.0", tun_gw],
                shell=True, capture_output=True, text=True
            )
            result2 = subprocess.run(
                ["route", "add", "128.0.0.0", "mask", "128.0.0.0", tun_gw],
                shell=True, capture_output=True, text=True
            )

            if result1.returncode != 0 or result2.returncode != 0:
                print("[VPN][route] 路由新增失敗：")
                if result1.stderr:
                    print(result1.stderr.strip())
                if result2.stderr:
                    print(result2.stderr.strip())

        except Exception as e:
            print(f"[VPN][route] 新增路由時發生錯誤: {e}")

    # 🆕 Debug 模式：印出出口 IP
    if DEBUG and not skip_ip_check:
        try:
            import requests
            ip = requests.get("https://ifconfig.me", timeout=5).text.strip()
            print(f"[VPN][debug] 當前出口 IP: {ip}")
        except Exception as e:
            print(f"[VPN][debug] 出口 IP 檢查失敗: {e}")

    return ResultCode.SUCCESS, {
        "pid": tun2socks_pid,
        "tun_gw": tun_gw,
        "interface_name": interface_name,
        "skip_ip_check": skip_ip_check
    }



def stop_vpn():
    """關閉 VPN（tun2socks）"""
    global _vpn_process

    if not _is_tun2socks_running():
        return ResultCode.SUCCESS, {"note": "VPN 未運行，略過停止"}

    try:
        if _vpn_process and _vpn_process.poll() is None:
            _vpn_process.terminate()
            _vpn_process.wait(timeout=5)
        subprocess.run(
            ["taskkill", "/F", "/IM", "tun2socks.exe"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
    except Exception as e:
        print(f"[VPN] 停止 VPN 失敗: {e}")
        return ResultCode.TASK_VPN_STOP_FAILED, None
    finally:
        _vpn_process = None

    return ResultCode.SUCCESS, None
