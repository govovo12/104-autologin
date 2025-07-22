from clockin_bot.clockin.cookie_loader import load_cookie_headers
import requests
from clockin_bot.clockin.base.result import ResultCode
url = "https://pro.104.com.tw/psc2"

result = load_cookie_headers()
if result.code != ResultCode.SUCCESS:
    print(f"❌ 無法載入 cookie headers：{result.message}")
    exit()

headers = result.data

resp = requests.get(url, headers=headers)
print(f"HTTP {resp.status_code}")

if "私人秘書" in resp.text or "打卡" in resp.text:
    print("✅ Cookie 有效，成功進入私人秘書打卡頁")
elif "登入" in resp.text or resp.status_code == 302:
    print("❌ Cookie 無效，被導向登入頁")
else:
    print("⚠️ 無法判斷是否登入成功，請人工查看")
    print(resp.text[:500])
try:
    resp = requests.get(url, headers=headers, timeout=5)
    print(f"HTTP {resp.status_code}")

    if "私人秘書" in resp.text or "打卡" in resp.text:
        print("✅ Cookie 有效，成功進入私人秘書打卡頁")
    elif "登入" in resp.text or resp.status_code == 302:
        print("❌ Cookie 無效，被導向登入頁")
    else:
        print("⚠️ 無法判斷是否登入成功，請人工查看")
        print(resp.text[:500])
except Exception as e:
    print(f"[ERROR] 發送 request 發生例外：{e}")
