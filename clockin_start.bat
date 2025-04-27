@echo off
start "" "C:\Program Files (x86)\Outline\Outline.exe"
timeout /t 8
cd /d C:\Users\user\Desktop\clockin-bot
call venv\Scripts\activate.bat
python scheduler_main.py
pause
