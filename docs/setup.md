# 🛠 安裝與環境建構說明（Setup Guide）

本文件將協助你從 0 建立好執行本專案所需的 Python 環境與必要資源，確保打卡流程可正常執行。

---

## ✅ 1. 環境需求

| 項目 | 說明 |
|------|------|
| 作業系統 | Windows 10 或以上 |
| Python 版本 | **3.11 或 3.13**（建議 64-bit） |
| 套件管理工具 | `pip`（Python 內建） |
| 建議工具 | VSCode / Terminal / PowerShell |

---

## ✅ 2. 建立虛擬環境（venv）

```bash
cd C:\Users\user\Desktop\104-autologin

# 建立虛擬環境
python -m venv venv

# 啟動虛擬環境（Windows）
venv\Scripts\activate
```

---

## ✅ 3. 安裝依賴套件

```bash
pip install -r requirements.txt
```

（如你尚未建立 `requirements.txt`，可使用 `pip freeze > requirements.txt` 產生）

---

## ✅ 4. 建立環境變數檔（.env）

請在專案根目錄建立 `.env` 檔案，格式如下：

```env
BOT_TOKEN=你的 Telegram Bot Token
CHAT_ID=你的 chat_id
```

> ✅ 範例格式請參考 `.env.example`

---

## ✅ 5. Shadowsocks 本地代理（sslocal）

本專案依賴 Shadowsocks 作為 socks5 proxy 進行打卡流程連線。

請手動下載 Shadowsocks 可執行檔並放置至以下路徑：

```
vpn/sslocal/
```

### 建議檔案：
- `sslocal.exe`
- `ss_config.json`（你的 socks5 配置檔案）

> 可參考：https://github.com/shadowsocks/shadowsocks-windows/releases  
> 若不使用代理功能，可跳過此步（打卡流程會失敗）

---

## ✅ 6. 登入並儲存 cookie（手動）

第一次使用請執行以下指令進行登入操作：

```bash
python run_clockin.py --task login_save_cookie
```

登入成功後會自動將狀態儲存至：

```
data/login_state.json
```

你也可以執行一條龍流程：

```bash
python run_clockin.py --task login_and_convert_cookie
```

會自動產生：
- `data/login_state.json`
- `data/cookie_header.json`

---

## ✅ 7. 執行主流程測試

確認一切安裝無誤後，可執行：

```bash
python run_clockin.py --task scheduler_main
```

你也可以使用 `.bat`：

```bat
scripts\run_task.bat         ← 輸入任務名稱（如 scheduler_main）
scripts\list_tasks.bat       ← 查看所有可用任務
```

---

## 🧪 附註：pytest 測試與覆蓋率

請參考 `docs/coverage.md` 與 `test/run_ci_like_tests.py` 以執行完整自動化測試流程。

---

## ✅ 完成！

你現在已經完成所有安裝步驟，可以開始使用本專案進行自動化打卡、測試、通知與擴充開發。
