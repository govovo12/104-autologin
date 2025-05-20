import os
import webbrowser
from pathlib import Path

def main():
    logs_dir = Path(__file__).resolve().parent.parent / "logs"
    if not logs_dir.exists():
        print("logs 資料夾不存在")
        return

    log_files = list(logs_dir.glob("*.log"))
    if not log_files:
        print("沒有任何 log 檔案")
        return

    latest_log = max(log_files, key=os.path.getmtime)
    html_output = logs_dir / "latest_log_view.html"

    with open(latest_log, "r", encoding="utf-8") as f:
        lines = f.readlines()

    html_content = "<html><head><meta charset='utf-8'><title>Latest Log</title></head><body style='font-family:monospace;'>"
    html_content += f"<h2>檔案：{latest_log.name}</h2><pre>"
    html_content += "".join(lines).replace("<", "&lt;").replace(">", "&gt;")
    html_content += "</pre></body></html>"

    with open(html_output, "w", encoding="utf-8") as f:
        f.write(html_content)

    webbrowser.open(f"file:///{html_output.as_posix()}")
    print(f"已開啟最新 log：{latest_log.name}")

if __name__ == "__main__":
    main()

