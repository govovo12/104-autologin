from playwright.async_api import Page

async def submit_login_form(page: Page, username: str, password: str) -> None:
    """
    自動填入帳號與密碼並提交登入表單。

    Args:
        page: Playwright 的 page 實例。
        username: 使用者帳號。
        password: 使用者密碼。
    """
    await page.wait_for_url("**/login**", timeout=60000)
    print(f"[DEBUG] 開始填寫登入資訊 username={username}")
    # 等待帳號欄位出現並輸入
    await page.wait_for_selector('input[type="text"]', timeout=10000)
    await page.fill('input[type="text"]', username)

    # 等待密碼欄位出現並輸入
    await page.wait_for_selector('input[type="password"]', timeout=10000)
    await page.fill('input[type="password"]', password)

    # 嘗試從多個候選選擇器中找到登入按鈕
    selectors = [
        'button[type="submit"]',
        'button:has-text("登入")',
        'text=登入',
    ]
    login_button = None
    for selector in selectors:
        try:
            login_button = await page.query_selector(selector)
            if login_button:
                print(f"[DEBUG] 使用選擇器登入按鈕：{selector}")
                await login_button.click()
                break
        except Exception:
            continue

    if not login_button:
        print("[WARNING] 找不到登入按鈕，請確認選擇器是否正確")

    # 稍作等待，避免畫面還沒反應就結束
    await page.wait_for_timeout(1000)
