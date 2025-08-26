# clockin_bot/tools/debug/gmail_login_helper.py

from clockin_bot.tools.email.gmail_verification import get_gmail_service_async

import asyncio

def entry():
    print("📬 啟動 Gmail 授權流程中...")
    asyncio.run(get_gmail_service_async(debug=True))

__task_info__ = {
    "desc": "手動執行 Gmail OAuth 驗證流程",
    "entry": entry,
}