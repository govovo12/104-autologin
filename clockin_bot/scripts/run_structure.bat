@echo off
cd %USERPROFILE%\Desktop\104-autologin
call venv\Scripts\activate
python run_clockin.py --task print_clean_structure
pause
