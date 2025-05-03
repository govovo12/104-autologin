@echo off
cd /d "%~dp0\.."
venv\Scripts\activate
python scripts\clockin_104.py
pause
