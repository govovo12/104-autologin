@echo off
cd /d %~dp0
cd ../..

echo 🚀 啟動 pytest 測試流程...

call venv\Scripts\activate.bat

python clockin_bot\test\run_ci_like_tests.py

if exist htmlcov\index.html (
    start htmlcov\index.html
)

pause

