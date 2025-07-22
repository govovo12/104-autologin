# clockin_bot/tools/debug/sid_tracker.py

from clockin_bot.tools.env_loader import get_env_var

DEBUG = get_env_var("DEBUG_MODE", "false").lower() == "true"


def track_sid_event(request_url: str, new_sid: str) -> None:
    """
    若 DEBUG_MODE 為 true，印出 connect.sid 被設定的請求來源與值。

    Args:
        request_url (str): 封包發出或設定 sid 的 URL。
        new_sid (str): 被設定的新 connect.sid 值。
    """
    if DEBUG:
        print(f"🍪 [SID] 被設定於：{request_url}")
        print(f"🔄 [SID] 新值：{new_sid}")
