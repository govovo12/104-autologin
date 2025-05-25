import os
import uuid
from datetime import datetime
from pathlib import Path
from clockin_bot.logger.safe_print import safe_print
def view_latest_log_html():
    logs_dir = Path(__file__).resolve().parent.parent.parent / "logs"
    latest_log = logs_dir / "latest_run.log"

    if not latest_log.exists():
        safe_print("❌ logs/latest_run.log 不存在")
        return

    safe_print(f"[DEBUG] 使用的來源是：{latest_log}")

    with open(latest_log, "r", encoding="utf-8") as f:
        lines = f.readlines()
        if lines:
            safe_print(f"[DEBUG] latest_run.log 最後一行：{lines[-1].strip()}")
        else:
            safe_print("[DEBUG] latest_run.log 是空的")

    html_output = Path(__file__).resolve().parent.parent.parent / "docs" / "latest_log_view.html"
    unique_id = uuid.uuid4()
    timestamp = datetime.now().isoformat()

    html_content = (
        "<html><head><meta charset='utf-8'><title>Latest Run Log</title></head>"
        "<body style='font-family:monospace;'>"
        f"<h2>來源：{latest_log.name}</h2><pre>"
        + "".join(lines).replace("<", "&lt;").replace(">", "&gt;")
        + f"\n<!-- generated at {timestamp} | id: {unique_id} -->\n"
        + "</pre></body></html>"
    )

    with open(html_output, "w", encoding="utf-8") as f:
        f.write(html_content)

    safe_print(f"✅ 已寫入 docs/latest_log_view.html")
    safe_print(f"DEBUG: timestamp={timestamp}, uuid={unique_id}")

__task_info__ = {
    "name": "view_latest_log",
    "desc": "以瀏覽器開啟 latest_run.log 的內容（HTML 格式）",
    "entry": view_latest_log_html,
}
