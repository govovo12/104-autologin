@echo off
cd %USERPROFILE%\Desktop\104-autologin
call venv\Scripts\activate
python run_clockin.py --task connect_ss_local
timeout /t 2 >nul
python run_clockin.py --task clockin_ss_test
pause
