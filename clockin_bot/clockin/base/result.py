from enum import Enum
from dataclasses import dataclass
from typing import Any, Optional

class ResultCode(Enum):
    # ✅ 成功
    SUCCESS = 0

    # ✅ cookie 相關錯誤
    COOKIE_NOT_FOUND = 1001         # 找不到 cookie 檔案
    COOKIE_EMPTY = 1002             # cookie 欄位為空或不存在
    COOKIE_LOAD_EXCEPTION = 1003    # 載入 cookie 發生例外

    # ✅ API 連線相關錯誤
    API_REQUEST_EXCEPTION = 2001    # requests.post 發生例外
    API_HTTP_ERROR = 2002           # HTTP 狀態碼非 200
    API_LOGIC_FAILED = 2003         # API 回傳邏輯失敗（例如 code != 200）

    # ✅ 回傳內容解析相關錯誤
    RESPONSE_PARSE_ERROR = 3001     # 回傳非 JSON 格式或無法解析
    ATT_ID_MISSING = 3002           # 回傳中缺少打卡 ID 欄位

    # ✅ 通知（Telegram）相關錯誤
    NOTIFY_FAILED = 9001            # 發送 Telegram 推播失敗
    NOTIFY_SKIP = 9002              # 未設定 TOKEN / CHAT_ID，略過推播

    # ✅ 未知錯誤
    UNKNOWN_ERROR = 9000            # 其他未分類錯誤
    
    # ✅ 排程跳過邏輯
    SKIP_TODAY = 8001  # 今天是假日或排除日，跳過排程

    # log / git upload 類型
    FILE_NOT_FOUND = 4001
    NO_CHANGE_TO_COMMIT = 4002
    GIT_ERROR = 4003
    # --- cookie check ---
    COOKIE_FILE_NOT_FOUND = 6001
    COOKIE_NO_VALID_EXPIRES = 6002
    COOKIE_ALREADY_EXPIRED = 6003
    COOKIE_PARSE_ERROR = 6004

    # --- VPN / SOCKS 錯誤 ---
    VPN_FILE_MISSING = 7001         # sslocal 或 config 檔案不存在
    VPN_START_TIMEOUT = 7002        # 嘗試啟動 10 秒失敗
    VPN_START_EXCEPTION = 7003      # Popen 發生錯誤
    VPN_STOP_FAILED = 7004          # 無法正常關閉 sslocal
    VPN_NOT_RUNNING = 7005          # 嘗試關閉時找不到 process


@dataclass
class TaskResult:
    code: ResultCode
    message: str
    data: Optional[Any] = None
