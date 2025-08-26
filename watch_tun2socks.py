import psutil
import time

def watch_tun2socks():
    print("[INFO] 開始監聽，請打開 Outline GUI 並手動連線 VPN...")
    seen = set()
    try:
        while True:
            for proc in psutil.process_iter(["pid", "name", "cmdline"]):
                if proc.info["name"] and "tun2socks.exe" in proc.info["name"].lower():
                    if proc.pid not in seen:
                        seen.add(proc.pid)
                        print(f"\n[FOUND] PID={proc.pid}")
                        print(" ".join(proc.info["cmdline"]))
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[INFO] 停止監聽")

if __name__ == "__main__":
    watch_tun2socks()
