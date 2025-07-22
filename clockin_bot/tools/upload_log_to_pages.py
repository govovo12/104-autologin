from datetime import datetime
from subprocess import run, CalledProcessError, PIPE
from pathlib import Path

from clockin_bot.logger.logger import get_logger
from clockin_bot.logger.decorators import log_call
from clockin_bot.notify.telegram_notify import send_telegram_message

log = get_logger("upload_log")

base_dir = Path(__file__).resolve().parent.parent.parent
latest_log_path = base_dir / "logs" / "latest_run.log"
html_path = base_dir / "docs" / "latest_log_view.html"

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="zh-Hant">
<head>
    <meta charset="UTF-8">
    <title>Log Viewer</title>
    <style>
        body {{ font-family: monospace; background: #f7f7f7; padding: 2rem; }}
        pre {{ background: #fff; padding: 1rem; border-radius: 6px; box-shadow: 0 0 8px rgba(0,0,0,0.1); }}
    </style>
</head>
<body>
    <h2>🧾 Latest Log - Generated {}</h2>
    <pre>{}</pre>
</body>
</html>
"""

@log_call
def upload_log_only():
    if not latest_log_path.exists():
        raise FileNotFoundError(f"❌ 找不到 log 檔：{latest_log_path}")

    html_path.parent.mkdir(parents=True, exist_ok=True)

    # 嘗試讀取 log（多編碼 fallback）
    try:
        print("[DEBUG] 嘗試以 UTF-8 讀取 log")
        log_text = latest_log_path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        try:
            print("[DEBUG] UTF-8 失敗，嘗試以 CP950")
            log_text = latest_log_path.read_text(encoding="cp950")
        except UnicodeDecodeError:
            print("[DEBUG] CP950 也失敗，改用 UTF-8 + errors=replace")
            log_text = latest_log_path.read_text(encoding="utf-8", errors="replace")

    # 產出 HTML
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    html_content = HTML_TEMPLATE.format(timestamp, log_text)
    html_path.write_text(html_content, encoding="utf-8")
    print(f"[DEBUG] ✅ HTML 已寫入：{html_path}")

    # Git 操作
    commit_msg = f"📄 更新報告 {timestamp}"
    try:
        run(["git", "add", str(html_path)], check=True)

        commit_result = run(
            ["git", "commit", "-m", commit_msg],
            stdout=PIPE, stderr=PIPE,
            text=True, encoding="utf-8", errors="replace"
        )

        output = (commit_result.stdout or "") + (commit_result.stderr or "")
        if "nothing to commit" in output.lower():
            print("⚠️ 沒有任何變更，略過推送")
        else:
            run(["git", "push"], check=True)
            print("✅ GitHub Pages 已推送")

            url = "https://govovo12.github.io/104-autologin/latest_log_view.html"
            send_telegram_message(f"📤 GitHub Pages 報告已更新\n🔗 {url}")

    except CalledProcessError as e:
        print(f"❌ Git 操作失敗：{e}")
        send_telegram_message("❌ GitHub Pages log 推送失敗，請手動確認錯誤")


__task_info__ = {
    "name": "upload_log_only",
    "desc": "將 latest_run.log 轉成 HTML 並推送至 GitHub Pages",
    "entry": upload_log_only,
}
