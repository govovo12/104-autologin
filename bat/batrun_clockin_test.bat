@echo off
cd /d "%~dp0\.."
call venv\Scripts\activate
python -m scripts.clockin_test_fullflow
pause
