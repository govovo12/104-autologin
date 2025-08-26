# clockin_bot/tools/common/result_code.py

# ===== ResultCode 常數區（分類依模組命名） =====
class ResultCode:
    # ✅ 通用成功
    SUCCESS = 0

    # 🔐 login 子控任務支線（10000 ~ 19999）
    TASK_LOAD_ENV_MISSING_KEY = 10003
    TASK_VPN_START_TIMEOUT = 10004
    TASK_NAVIGATE_FAILED = 10005  # 無法打開登入頁，可能是 URL 錯誤或網路異常
    TASK_BROWSER_LAUNCH_FAILED = 10006

    # step_5_submit_login.py
    TASK_SUBMIT_LOGIN_FAILED = 10007

    # step_6_wait_login_request.py
    TASK_WAIT_LOGIN_REQUEST_TIMEOUT = 10008  # 等待登入帳密封包（/oauth2/login）逾時

    # step_10_wait_for_sid_cookie.py
    TASK_SID_COOKIE_NOT_FOUND = 10009  # 等待 connect.sid cookie 失敗

    # step_11_convert_cookie_header.py
    TASK_CONVERT_COOKIE_HEADER_FAILED = 10010  # 抓取 cookies 或轉換 header 失敗

    # step_12_save_login_state.py
    TASK_SAVE_LOGIN_STATE_FAILED = 10013  # 儲存 login_state 檔案失敗

    # clockin_bot/vpn 子控任務（10020 ~ 10029）
    TASK_VPN_ENV_MISSING_KEY = 10020      # 缺少必要 VPN 環境變數
    TASK_VPN_CONFIG_FILE_NOT_FOUND = 10021  # VPN 設定檔不存在
    TASK_VPN_CONFIG_INVALID_FORMAT = 10022  # VPN 設定檔格式錯誤（缺少 exe_path / params）
    TASK_VPN_PROCESS_NOT_FOUND = 10023    # 未偵測到 tun2socks 進程
    TASK_VPN_TUN_GW_MISSING = 10024       # 無法從參數找到 -tunGw
    TASK_VPN_ROUTE_ADD_FAILED = 10025     # 設定路由失敗
    TASK_VPN_STOP_FAILED = 10026          # 關閉 tun2socks 失敗
    # clockin_bot/vpn 子控任務（10020 ~ 10029）
    TASK_VPN_INVALID_ACTION = 10027  # VPN 控制器 action 無效

    # clockin_bot/modules/scheduler 子控任務（10030 ~ 10039）
    TASK_SKIP_TODAY = 10030  # 打卡任務：今天不執行（假日或設定跳過）


    # 🧰 工具模組錯誤支線（40000 ~ 49999）
    # log_helper.py 目前無錯誤碼需求

    # 🔐 tools/email/gmail_verification.py（40010 ~ 40019）
    TOOLS_TASK_FETCH_VERIFICATION_CODE_FAILED = 40010

    # tools/page/input_verification_code.py（41030 ~ 41039）
    TOOLS_INPUT_VERIFICATION_CODE_FAILED = 41030  # Playwright 輸入驗證碼失敗

    # step_9_wait_for_redirect.py
    TOOLS_WAIT_FOR_PSC2_FAILED = 41040  # 等待 /psc2 導向失敗


# ===== 錯誤分類集合（供 log_helper 判斷用途） =====
SUCCESS_CODES = {
    ResultCode.SUCCESS,
}

TASK_ERROR_CODES = {
    ResultCode.TASK_LOAD_ENV_MISSING_KEY,
    ResultCode.TASK_VPN_START_TIMEOUT,
    ResultCode.TASK_NAVIGATE_FAILED,
    ResultCode.TASK_BROWSER_LAUNCH_FAILED,
    ResultCode.TASK_SUBMIT_LOGIN_FAILED,
    ResultCode.TASK_WAIT_LOGIN_REQUEST_TIMEOUT,
    ResultCode.TASK_SID_COOKIE_NOT_FOUND,
    ResultCode.TASK_CONVERT_COOKIE_HEADER_FAILED,
    ResultCode.TASK_SAVE_LOGIN_STATE_FAILED,
    ResultCode.TASK_VPN_ENV_MISSING_KEY,
    ResultCode.TASK_VPN_CONFIG_FILE_NOT_FOUND,
    ResultCode.TASK_VPN_CONFIG_INVALID_FORMAT,
    ResultCode.TASK_VPN_PROCESS_NOT_FOUND,
    ResultCode.TASK_VPN_TUN_GW_MISSING,
    ResultCode.TASK_VPN_ROUTE_ADD_FAILED,
    ResultCode.TASK_VPN_STOP_FAILED,
    ResultCode.TASK_VPN_INVALID_ACTION,
    ResultCode.TASK_SKIP_TODAY,


}


TOOL_ERROR_CODES = {
    ResultCode.TOOLS_TASK_FETCH_VERIFICATION_CODE_FAILED,
    ResultCode.TOOLS_INPUT_VERIFICATION_CODE_FAILED,
    ResultCode.TOOLS_WAIT_FOR_PSC2_FAILED,
}



# ===== 錯誤碼訊息字典（供 log_helper 印出） =====
ERROR_MESSAGES = {
    ResultCode.SUCCESS: "通用成功",
    ResultCode.TASK_LOAD_ENV_MISSING_KEY: "環境變數設定錯誤，缺少必要欄位。",
    ResultCode.TASK_VPN_START_TIMEOUT: "VPN 啟動逾時，請檢查 Shadowsocks 狀態或網路設定。",
    ResultCode.TASK_NAVIGATE_FAILED: "無法打開登入頁，請確認 URL 或網路狀態",
    ResultCode.TASK_BROWSER_LAUNCH_FAILED: "無法啟動瀏覽器或建立分頁",
    ResultCode.TASK_SUBMIT_LOGIN_FAILED: "登入表單提交失敗（帳密欄位不存在或無法點擊）",
    ResultCode.TASK_WAIT_LOGIN_REQUEST_TIMEOUT: "等待帳密登入封包逾時，未偵測到 /oauth2/login 請求",
    ResultCode.TOOLS_TASK_FETCH_VERIFICATION_CODE_FAILED: "tools: 抓取 Gmail 驗證碼失敗",
    ResultCode.TOOLS_INPUT_VERIFICATION_CODE_FAILED: "tools: 輸入 Gmail 驗證碼失敗",
    ResultCode.TOOLS_WAIT_FOR_PSC2_FAILED: "tools: 等待登入導向 /psc2 超時失敗",
    ResultCode.TASK_SID_COOKIE_NOT_FOUND: "task: 未能擷取 connect.sid cookie",
    ResultCode.TASK_CONVERT_COOKIE_HEADER_FAILED: "task: 無法抓取 cookies 或轉換為 header 格式",
    ResultCode.TASK_SAVE_LOGIN_STATE_FAILED:"task: 儲存 login_state 檔案失敗（可能是權限或格式問題）",
    ResultCode.TASK_VPN_ENV_MISSING_KEY: "VPN 環境變數缺失，請檢查 .env 設定",
    ResultCode.TASK_VPN_CONFIG_FILE_NOT_FOUND: "VPN 設定檔不存在，請確認 VPN_CONFIG_PATH",
    ResultCode.TASK_VPN_CONFIG_INVALID_FORMAT: "VPN 設定檔格式錯誤（缺少 exe_path 或 params）",
    ResultCode.TASK_VPN_PROCESS_NOT_FOUND: "VPN 啟動後未偵測到 tun2socks 進程",
    ResultCode.TASK_VPN_TUN_GW_MISSING: "無法從參數找到 -tunGw，無法設定全域路由",
    ResultCode.TASK_VPN_ROUTE_ADD_FAILED: "設定全域路由失敗",
    ResultCode.TASK_VPN_STOP_FAILED: "關閉 tun2socks 進程失敗",
    ResultCode.TASK_VPN_INVALID_ACTION: "VPN 控制器 action 無效（必須為 start 或 stop）",
    ResultCode.TASK_SKIP_TODAY: "打卡任務：今天不執行（假日或設定跳過）",



}
