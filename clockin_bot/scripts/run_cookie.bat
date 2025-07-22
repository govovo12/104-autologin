@echo off
cd /d C:\Users\user\Desktop\104-autologin
call venv\Scripts\activate
python run_clockin.py --task session_controller
