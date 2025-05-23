import os
from pathlib import Path
from dotenv import load_dotenv

# ✅ 直接載入 .env（不再判斷 GitHub）
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
STORAGE_STATE_PATH = str(BASE_DIR / "data" / "login_state.json")

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
