# clockin_bot/tools/env/env_loader.py

import os
from dotenv import load_dotenv

load_dotenv()


def get_env_var(key: str, default: str = "") -> str:
    """
    取得指定的環境變數，若未設定則回傳預設值。

    Args:
        key (str): 環境變數名稱
        default (str): 預設值（當環境變數不存在時使用）

    Returns:
        str: 取得的環境變數值
    """
    return os.getenv(key, default)
