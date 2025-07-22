import asyncio

async def wait_for_request_by_url(
    page,
    url_keyword: str,
    method: str = None,
    timeout: int = 15000,
    debug: bool = False
) -> bool:
    """
    等待某個包含指定 URL 關鍵字的請求被送出。

    Args:
        page: Playwright 的 page 實例
        url_keyword: URL 中關鍵字（例如 /oauth2/login、/psc2）
        method: 限制特定 HTTP 方法（例如 "POST"），預設不限制
        timeout: 等待時間（毫秒）
        debug: 是否開啟除錯模式

    Returns:
        True：成功捕捉到符合條件的請求
        False：逾時未捕捉到
    """
    event = asyncio.Event()

    def handle_request(request):
        if url_keyword in request.url:
            if method and request.method != method:
                return
            if debug:
                print(f"[DEBUG] 捕捉到請求：{request.method} {request.url}")
            event.set()

    page.on("request", handle_request)

    try:
        await asyncio.wait_for(event.wait(), timeout / 1000)
        return True
    except asyncio.TimeoutError:
        if debug:
            print(f"⚠️ 等待請求逾時：{method or '*'} {url_keyword}")
        return False
