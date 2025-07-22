import json
from pathlib import Path
from clockin_bot.clockin.base.result import TaskResult, ResultCode


def load_login_state() -> TaskResult:
    """
    單純讀取 login_state.json 的內容（格式可能是 cookie list 或 header）
    不進行轉換，由上層模組依需求判斷格式後自行轉換。
    """
    try:
        file_path = Path("clockin_bot/data/login_state.json")
        if not file_path.exists():
            return TaskResult(ResultCode.COOKIE_NOT_FOUND, "找不到 login_state.json")

        with open(file_path, encoding="utf-8") as f:
            data = json.load(f)

        # 僅驗證資料型別是我們能接受的格式（list 或 dict）
        if not isinstance(data, (list, dict)):
            return TaskResult(ResultCode.COOKIE_EMPTY, "login_state.json 格式錯誤（應為 list 或 dict）")

        return TaskResult(ResultCode.SUCCESS, "已成功載入 login_state", data)

    except Exception as e:
        return TaskResult(ResultCode.COOKIE_LOAD_EXCEPTION, f"載入 login_state 發生例外：{e}")
