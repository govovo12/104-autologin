from clockin_bot.tools.page.input_verification_code import input_verification_code
from clockin_bot.tools.common.result_code import ResultCode


async def step_8_input_verification_code(page, verification_code: str, debug: bool = False) -> int:
    """
    Step 8：在驗證頁面輸入六位驗證碼。

    Args:
        page: Playwright 的 page 實例
        verification_code: 擷取到的驗證碼字串
        debug: 是否開啟除錯模式

    Returns:
        int: 錯誤碼（成功為 ResultCode.SUCCESS，其餘為工具回傳錯誤碼）
    """
    code = await input_verification_code(
        page=page,
        code=verification_code,
        debug=debug
    )
    return code
