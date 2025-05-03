@echo off
cd /d "%~dp0\.."

:: 啟動虛擬環境
call venv\Scripts\activate

:: 用 module 方式啟動小PY，保證正確路徑
python -m scripts.outline_connect_only

timeout /t 5

:: 再啟動check cookie
python -m scripts.check_cookie_expiry_v2

pause


