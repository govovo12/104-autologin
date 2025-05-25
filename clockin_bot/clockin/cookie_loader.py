from pathlib import Path
import json
from clockin_bot.clockin.base.result import TaskResult, ResultCode
from clockin_bot.logger.logger import get_logger
from clockin_bot.logger.decorators import log_call

log = get_logger("cookie")

@log_call
def load_cookie_headers() -> TaskResult:
    try:
        # 這裡直接指定絕對路徑
        cookie_path = Path(r"C:\Users\user\Desktop\104-autologin\clockin_bot\data\cookie_header.json")

        if not cookie_path.exists():
            return TaskResult(
                code=ResultCode.COOKIE_NOT_FOUND,
                message="找不到 cookie_header.json 檔案"
            )

        with open(cookie_path, encoding="utf-8") as f:
            cookie_str = json.load(f).get("cookie")
            if not cookie_str:
                return TaskResult(
                    code=ResultCode.COOKIE_EMPTY,
                    message="cookie 欄位為空或不存在"
                )

        headers = {
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0",
            "cookie": cookie_str
        }

        return TaskResult(
            code=ResultCode.SUCCESS,
            message="成功載入 cookie headers",
            data=headers
        )

    except Exception as e:
        return TaskResult(
            code=ResultCode.COOKIE_LOAD_EXCEPTION,
            message=f"載入 cookie 發生例外：{e}"
        )

__task_info__ = {
    "name": "load_cookie_headers",
    "desc": "讀取 cookie_header.json 並回傳標準 headers 結構",
    "entry": load_cookie_headers,
}
