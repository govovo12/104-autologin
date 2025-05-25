# 🕹️ 104 自動打卡系統（Clock-in Automation Framework）

本專案為一套 **自動打卡至 104.com.tw 的模組化架構系統**，結合 VPN Proxy、Cookie 登入、Retry 機制與 Telegram 通知，支援單元測試、整合測試與 E2E 流程。

> 💼 適合展示 Python 自動化能力、任務註冊設計、測試整合與 CLI 工具設計能力。

---

## ✅ 功能特色

- 🧩 任務模組化：所有功能皆以 `__task_info__` 註冊，可 CLI 單獨執行
- 🧠 支援 Retry：API 可重試 + 自動失敗通知
- 📅 假日判斷：透過 holiday.json 判定是否略過執行
- 🌐 VPN 整合：使用 Shadowsocks 本地啟動 socks5 proxy
- 📢 Telegram 通知：打卡成功 / 失敗自動推播訊息
- 🧪 pytest 測試整合：含 CI 模擬、覆蓋率報表產生
- 💻 支援 `.bat` 快捷執行，不懂 Python 也能用

---

## 🚀 快速開始

```bash
# 1. 建立虛擬環境
python -m venv venv
venv\Scripts\activate

# 2. 安裝依賴套件
pip install -r requirements.txt

# 3. 執行任務（例如打卡）
python run_clockin.py --task clockin_104
```

或使用 `.bat` 快捷啟動：

```bat
scripts\run_task.bat        ← 啟動任務（輸入名稱）
scripts\list_tasks.bat      ← 查看所有可執行任務
scripts\run_main.bat        ← 執行主流程（scheduler_main）
```

---

## 🧾 文件導覽（docs/）

| 文件 | 說明 |
|------|------|
| [`docs/setup.md`](docs/setup.md) | 安裝、環境建置、VPN 配置與 Cookie 儲存說明 |
| [`docs/run_instructions.md`](docs/run_instructions.md) | 如何執行任務、使用 `.bat` 或 CLI |
| [`docs/tasks_list.md`](docs/tasks_list.md) | 所有 `__task_info__` 任務清單與功能說明 |
| [`docs/coverage.md`](docs/coverage.md) | 測試覆蓋率與本地 CI 測試控制器 |
| [`docs/test_strategy.md`](docs/test_strategy.md) | 測試策略設計、邏輯覆蓋與未來擴充建議 |

---

## 📂 任務一覽（可執行模組）

| 任務名稱 | 描述 |
|----------|------|
| `scheduler_main` | 主流程控制器：VPN → 打卡 → 通知 |
| `clockin_104` | 發送打卡 API |
| `login_save_cookie` | 開啟瀏覽器手動登入並儲存 login_state.json |
| `convert_login_cookie` | 將 login_state 轉換為 cookie_header.json |
| `login_and_convert_cookie` | 一條龍執行登入 + 轉換 cookie |
| `check_cookie_expiry_v2` | 分析 cookie 剩餘效期狀態 |
| `list_tasks` | 顯示所有可執行任務清單 |

---

## 🧪 測試說明

```bash
# 執行三階段測試 + coverage
python -m clockin_bot.test.run_ci_like_tests

# coverage 報表位置
htmlcov/index.html
```

- 所有 log 與 pytest 結果將輸出至 `logs/` 目錄
- pytest 覆蓋率可透過 pytest-cov 統計

---

## 🔐 敏感檔案（不推 GitHub）

| 路徑 | 用途 |
|------|------|
| `data/login_state.json` | Playwright 儲存的登入狀態 |
| `data/cookie_header.json` | 已轉換的 Cookie Header |
| `vpn/sslocal/*.exe` | Shadowsocks 執行檔（請自行下載） |
| `.env` | Telegram bot token 等憑證（僅提供 `.env.example` 範例）

---

## 👷 作者資訊

- 開發者：湯尼（Tony）｜測試工程師
- 技術關鍵字：Python、requests、Playwright、Shadowsocks、pytest、Telegram bot、自動化腳本架構

---

---

## 🔐 注意事項：不包含於 GitHub 的本地檔案

請記得手動建立以下檔案或資料，以確保專案可執行：

| 檔案 / 資料夾 | 用途 |
|----------------|------|
| `.env` | Telegram bot token 與 chat_id |
| `data/login_state.json` | Playwright 登入儲存檔，透過登入流程自動產生 |
| `data/cookie_header.json` | Cookie Header 轉換檔，透過轉換流程自動產生 |
| `vpn/sslocal/*.exe` | Shadowsocks 可執行檔，請手動下載放置 |




## 🏁 專案狀態

✅ 已完成：打卡流程自動化、模組註冊機制、測試整合與通知  
🚧 計畫中：將本專案架構用於其他 API 專案作為展示作品延伸

