"""
Step 13: 關閉 Playwright 與相關資源
此模組負責在任務結尾階段，釋放所有 Playwright 相關資源以避免資源洩漏。
"""
from clockin_bot.tools.common.result_code import ResultCode
    
async def run_step_13_release_playwright(context_data: dict) -> tuple:
    """
    關閉 browser、context 和 playwright 實例，釋放資源

    Args:
        context_data (dict): 子控制器傳入的 context 共享資料

    Returns:
        tuple: (錯誤碼, 空字串)
    """
    try:
        if context := context_data.get("context"):
            await context.close()
        if browser := context_data.get("browser"):
            await browser.close()
        if playwright := context_data.get("playwright"):
            await playwright.stop()
        return ResultCode.SUCCESS, ""
    except Exception:
        return ResultCode.TASK_EXCEPTION, 