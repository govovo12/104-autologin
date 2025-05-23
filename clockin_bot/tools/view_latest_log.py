import os
import uuid
from datetime import datetime
from pathlib import Path

def view_latest_log_html():
    logs_dir = Path(__file__).resolve().parent.parent.parent / "logs"
    if not logs_dir.exists():
        print("logs 資料夾不存在")
        return

    log_files = list(logs_dir.glob("*.log"))
    if not log_files:
        print("沒有任何 log 檔案")
        return

    latest_log = max(log_files, key=os.path.getmtime)
    html_output = Path(__file__).resolve().parent.parent.parent / "docs" / "latest_log_view.html"

    with open(latest_log, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # 構造 HTML，強制加入唯一且每次都會變的隨機字串
    unique_id = uuid.uuid4()
    timestamp = datetime.now().isoformat()
    html_content = (
        "<html><head><meta charset='utf-8'><title>Latest Log</title></head>"
        "<body style='font-family:monospace;'>"
        f"<h2>檔案：{latest_log.name}</h2><pre>"
        + "".join(lines).replace("<", "&lt;").replace(">", "&gt;")
        + f"\n<!-- generated at {timestamp} | id: {unique_id} -->\n"
        + "</pre></body></html>"
    )

    with open(html_output, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"✅ 已開啟最新 log：{latest_log.name}")
    print(f"DEBUG: 寫入的 timestamp={timestamp}, uuid={unique_id}")

__task_info__ = {
    "name": "view_latest_log",
    "desc": "以瀏覽器開啟最新執行 log（HTML 格式）",
    "entry": view_latest_log_html,
}
