# clockin_bot/logger/safe_print.py

import builtins  

def safe_print(*args, **kwargs):
    try:
        builtins.print(*args, **kwargs)
    except UnicodeEncodeError:
        clean_args = [str(arg).encode("ascii", errors="ignore").decode() for arg in args]
        builtins.print(*clean_args, **kwargs)
