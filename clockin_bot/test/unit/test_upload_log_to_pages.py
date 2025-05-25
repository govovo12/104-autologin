import pytest
from unittest.mock import MagicMock
import clockin_bot.tools.upload_log_to_pages as upload_log_to_pages

def test_upload_log_success(tmp_path, monkeypatch):
    """測試正常情況下能成功 push"""
    docs_path = tmp_path / "docs"
    docs_path.mkdir()
    html_path = docs_path / "latest_log_view.html"
    html_path.write_text("<html>log</html>", encoding="utf-8")

    mock_run = MagicMock()
    mock_run.return_value.returncode = 1  # 模擬有 staged file
    monkeypatch.setattr(upload_log_to_pages, "subprocess", MagicMock(run=mock_run))
    monkeypatch.setattr(upload_log_to_pages, "Path", lambda *a, **kw: tmp_path)

    upload_log_to_pages.upload_log_only()

def test_upload_log_skipped(monkeypatch, tmp_path):
    """測試沒有任何變更會跳過 commit"""
    docs_path = tmp_path / "docs"
    docs_path.mkdir()
    html_path = docs_path / "latest_log_view.html"
    html_path.write_text("dummy", encoding="utf-8")

    def run_mock(cmd, **kwargs):
        if "diff" in cmd:
            return MagicMock(returncode=0)  # 模擬沒有變更
        return MagicMock(returncode=1)

    monkeypatch.setattr(upload_log_to_pages, "subprocess", MagicMock(run=run_mock))
    monkeypatch.setattr(upload_log_to_pages, "Path", lambda *a, **kw: tmp_path)

    upload_log_to_pages.upload_log_only()

def test_upload_log_missing_file(monkeypatch, tmp_path):
    """測試找不到報告檔案時應跳過"""
    monkeypatch.setattr(upload_log_to_pages, "Path", lambda *a, **kw: tmp_path)
    upload_log_to_pages.upload_log_only()
