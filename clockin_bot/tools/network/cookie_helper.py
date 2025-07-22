# tools/network/cookie_helper.py

import json
from typing import List

from playwright.async_api import BrowserContext
from typing import List


async def fetch_browser_cookies(context: BrowserContext) -> List[dict]:
    """
    從指定的 Playwright context 抓取目前所有 cookies。

    Args:
        context (BrowserContext): 瀏覽器 context 實例

    Returns:
        List[dict]: 所有 cookies 的清單
    """
    return await context.cookies()


def convert_cookies_to_header(cookies: List[dict]) -> dict:
    """
    將 cookies（list of dict）轉換為 header 格式
    """
    cookie_str = "; ".join(f"{c['name']}={c['value']}" for c in cookies)
    return {"Cookie": cookie_str}

def save_cookies_to_file(cookies: List[dict], file_path: str):
    """
    將 cookies 儲存為 JSON 檔
    """
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(cookies, f, indent=2, ensure_ascii=False)

def load_cookies_from_file(file_path: str) -> List[dict]:
    """
    載入儲存的 cookies JSON 檔
    """
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)
    
def save_headers_to_file(headers: dict, file_path: str):
    """
    將 headers（包含 Cookie 欄位）儲存為 JSON 檔
    """
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(headers, f, indent=2, ensure_ascii=False)
