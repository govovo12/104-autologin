@echo off
cd /d C:\Users\user\Desktop\104-autologin
set /p TASK=Enter task name to run (e.g., clockin_104):
venv\Scripts\python.exe run_clockin.py --task %TASK%
pause
