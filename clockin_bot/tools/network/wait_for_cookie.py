import asyncio
import time
from playwright.async_api import BrowserContext

async def wait_for_cookie_updated(name: str, context: BrowserContext, domain: str, timeout: int = 10) -> dict | None:
    """
    等待指定 cookie 被多次設定，回傳最後一筆有效版本。
    """
    print(f"🕒 等待 cookie「{name}」寫入記錄（domain={domain}，最多 {timeout} 秒）...")

    sid_records = []

    async def handle_response(response):
        try:
            headers = await response.all_headers()
            set_cookie = headers.get("set-cookie", "")
            if f"{name}=" in set_cookie and domain in response.url:
                sid_value = set_cookie.split(f"{name}=")[1].split(";")[0]
                timestamp = time.time()
                sid_records.append({
                    "value": sid_value,
                    "url": response.url,
                    "timestamp": timestamp
                })
                print(f"🍪 [SID] 被設定於：{response.url}")
                print(f"🔄 [SID] 新值：{sid_value}")
        except Exception as e:
            print(f"[Error] sid 解析失敗：{e}")

    context.on("response", handle_response)

    # 等待指定時間內可能出現的多次 sid 設定
    await asyncio.sleep(timeout)

    if not sid_records:
        print(f"[❗] 在 {timeout} 秒內沒有偵測到任何 sid 設定")
        return None

    # 取出最後出現的那一筆
    last = max(sid_records, key=lambda r: r["timestamp"])
    print(f"[✅] 最終有效 sid 來自：{last['url']}")
    return {
        "name": name,
        "value": last["value"]
    }
