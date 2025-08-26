import os
from pathlib import Path
from dotenv import load_dotenv
from dotenv import dotenv_values

# 專案根目錄
ROOT_DIR = Path(__file__).resolve().parents[2]

# 載入 .env
load_dotenv(ROOT_DIR / ".env")


def get_env_var(key: str, default: str = None) -> str:
    """
    回傳 .env 變數值，找不到就回傳 default
    """
    return os.getenv(key, default)


def get_abs_path_from_env(key: str) -> Path:
    """
    讀取 .env 變數並轉為以 ROOT_DIR 為基準的絕對路徑
    """
    value = os.getenv(key)
    if not value:
        raise ValueError(f"❌ 無法從 .env 找到鍵：{key}")
    return ROOT_DIR / value

def get_all_env_vars() -> dict:
    """
    取得 .env 檔案中定義的所有變數 (key-value)
    """
    return dotenv_values(ROOT_DIR / ".env")
