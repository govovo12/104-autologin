import pytest
from clockin_bot.tools.retry_runner import run_with_retry
from clockin_bot.clockin.base.result import TaskResult, ResultCode

def test_success_on_first_try():
    # 模擬一開始就成功
    def task():
        return TaskResult(code=ResultCode.SUCCESS, message="OK")

    result = run_with_retry(task, retry=3)
    assert result.code == ResultCode.SUCCESS

def test_success_on_third_try():
    # 模擬前兩次失敗，第3次成功
    state = {"count": 0}

    def flaky_task():
        state["count"] += 1
        if state["count"] < 3:
            return TaskResult(code=ResultCode.API_REQUEST_EXCEPTION, message="fail")
        return TaskResult(code=ResultCode.SUCCESS, message="OK")

    result = run_with_retry(flaky_task, retry=5)
    assert result.code == ResultCode.SUCCESS
    assert state["count"] == 3

def test_fail_all_retries():
    # 模擬所有重試都失敗
    def always_fail():
        return TaskResult(code=ResultCode.API_REQUEST_EXCEPTION, message="still bad")

    result = run_with_retry(always_fail, retry=3)
    assert result.code == ResultCode.API_REQUEST_EXCEPTION
