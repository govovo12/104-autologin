from clockin_bot.tools.common.result_code import ResultCode


async def input_verification_code(page, code: str, debug: bool = False) -> int:
    """
    在驗證碼頁面輸入六位驗證碼，回傳錯誤碼。

    Args:
        page: Playwright 的 page 實例
        code: 驗證碼字串
        debug: 是否開啟 debug 印出

    Returns:
        int: 錯誤碼
    """
    try:
        if debug:
            print(f"開始輸入驗證碼：{code}")

        await page.wait_for_selector('input', timeout=10000)
        await page.click('input')
        await page.keyboard.type(code)
        await page.wait_for_timeout(1000)

        return ResultCode.SUCCESS

    except Exception as e:
        if debug:
            print(f"輸入驗證碼時發生錯誤：{e}")
        return ResultCode.TOOLS_INPUT_VERIFICATION_CODE_FAILED
