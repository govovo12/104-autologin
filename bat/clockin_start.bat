cd /d C:\Users\user\Desktop\clockin-bot
call venv\Scripts\activate.bat
python -m scripts.scheduler_main
timeout /t 10 /nobreak
exit
