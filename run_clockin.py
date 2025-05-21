# run_clockin.py
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent / "clockin_bot"))

from clockin_bot.modules.scheduler.scheduler_main import main

if __name__ == "__main__":
    main()
