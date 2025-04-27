@echo off
cd /d C:\Users\user\Desktop\clockin-bot
call venv\Scripts\activate.bat
python check_cookie_alive.py
pause
