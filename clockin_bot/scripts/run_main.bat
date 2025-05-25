@echo off
cd /d "%~dp0\..\.."
call venv\Scripts\activate
python -m clockin_bot.modules.scheduler.scheduler_main
pause
