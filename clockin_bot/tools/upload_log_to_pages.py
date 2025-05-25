import subprocess
from datetime import datetime
from pathlib import Path
from clockin_bot.clockin.base.result import TaskResult, ResultCode
from clockin_bot.logger.logger import get_logger
from clockin_bot.logger.decorators import log_call

log = get_logger("uploader")

@log_call
def upload_log_only() -> TaskResult:
    base_dir = Path(__file__).resolve().parent.parent.parent
    html_path = base_dir / "docs" / "latest_log_view.html"

    # 若報告檔不存在，回傳 FILE_NOT_FOUND 錯誤碼
    if not html_path.exists():
        msg = "找不到報告檔 docs/latest_log_view.html"
        log.warning(msg)
        return TaskResult(code=ResultCode.FILE_NOT_FOUND, message=msg)

    try:
        # 加入 staged 區域
        subprocess.run(["git", "add", str(html_path)], check=True)

        # 檢查是否有變更加入 staged 區域，若沒有就跳過
        result = subprocess.run(["git", "diff", "--cached", "--quiet"])
        if result.returncode == 0:
            msg = "沒有任何變更加入暫存區，跳過 commit。"
            log.info(msg)
            return TaskResult(code=ResultCode.NO_CHANGE_TO_COMMIT, message=msg)

        # 有變更 → commit + push
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        subprocess.run(["git", "commit", "-m", f"📄 更新報告 {timestamp}"], check=True)
        subprocess.run(["git", "push"], check=True)

        msg = "已推送報告至 GitHub Pages"
        log.info(msg)
        return TaskResult(code=ResultCode.SUCCESS, message=msg)

    except subprocess.CalledProcessError as e:
        # Git 指令出錯
        msg = f"Git 操作失敗：{e}"
        log.error(msg)
        return TaskResult(code=ResultCode.GIT_ERROR, message=msg)

__task_info__ = {
    "name": "upload_log_only",
    "desc": "將報告檔（HTML）推送至 GitHub Pages（如果有變更）",
    "entry": upload_log_only
}
