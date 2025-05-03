@echo off
cd /d "%~dp0\.."
call venv\Scripts\activate
python print_clean_structure.py
pause
