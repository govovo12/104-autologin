# clockin-bot 使用說明（完整專業版 README）

## 0. 建立虛擬環境 (venv)

### (1) 進入 clockin-bot 資料夾

```bash
cd C:\Users\你的使用者名稱\Desktop\clockin-bot
```

### (2) 創建虛擬環境

```bash
python -m venv venv
```

完成後，資料夾裡會多一個 `venv/`。

### (3) 啟動虛擬環境

```bash
venv\Scripts\activate
```

✅ Terminal 看到 `(venv)`，代表啟動成功！

### (4) 安裝必要套件

```bash
pip install playwright pyautogui pytesseract requests pillow pygetwindow keyboard
playwright install
```

✅ 一次安裝所有需要的東西。

---

## 1. 必要設定

- 打開 `config.py`
  - 設定 Telegram Bot Token
  - 設定 Telegram Chat ID
  - 設定 Outline.exe 路徑（根據你的安裝路徑）
  - 設定 Tesseract-OCR 的執行檔路徑（根據你的安裝路徑）

- 執行 `login_save_cookie.py`
  - 手動登入 104，成功後按 Enter
  - 產生 `login_state.json` 保存登入狀態

---

## 2. 每日使用流程

- 每日打卡流程：
  - 排程或手動執行 `scheduler_main.py`
  - 自動打開 VPN ➔ 自動打卡 ➔ 成功通知 Telegram

- 每月 cookie 檢查：
  - 每月10號排程執行 `check_cookie_alive.py`
  - 自動檢查 cookie 是否失效
  - 成功或失敗都會通知 Telegram

---

## 3. 注意事項

- **螢幕解析度或比例改變時**，需重新用 `record_positions.py` 記錄 Outline 按鈕座標。
- **更換104帳號或密碼時**，需重新執行 `login_save_cookie.py` 保存新的 login_state.json。
- **更換電腦時**，記得把整個 clockin-bot 資料夾一起搬走（包含 venv/、所有.py檔）。

---

# clockin-bot 資料夾結構

| 檔案/資料夾             | 功能說明 |
|:-------------------------|:---------|
| venv/                     | Python 虛擬環境資料夾 |
| __pycache__/              | Python 快取資料夾 |
| config.py                 | 共用設定（TOKEN、路徑等）⚡ 必須改 |
| check_cookie_alive.py     | 每月自動檢查 login_state.json 是否有效 |
| clockin_104.py             | 104 打卡流程（使用保存的 cookie） |
| login_save_cookie.py      | 手動登入104並保存cookie檔案 |
| login_state.json          | 104 登入後保存的 cookie ⚡ 每個帳號不同 |
| outline_connect.py        | 自動開啟 Outline VPN 並偵測連線狀態 ⚡ 確認 Outline.exe路徑正確 |
| record_positions.py       | 手動記錄 Outline 按鈕座標 ⚡ 不同螢幕解析度需重錄 |
| scheduler_main.py         | 打卡總控排程（整合 VPN連線+104打卡） |
| telegram_notify.py        | 發送Telegram通知（自動加上時間戳） |
| test_login_state.py       | 測試login_state.json是否還有效的小工具 |
| utils_delay.py            | 隨機延遲模組（控制打卡時間範圍） |
| vpn_outline_connect.py    | VPN連線模組（呼叫Outline Connect流程） |

---
🔥 更新：加入 .bat 啟動 + 排程器設定！
現在改成由 clockin_start.bat 啟動 Outline 和打卡流程。

請用 Windows 工作排程器，設定排程指向 clockin_start.bat。

排程設定時務必勾選「以最高權限執行」。

Outline.exe 必須事先安裝在 C:\Program Files (x86)\Outline。

clockin_start.bat 會自動打開 Outline，等待8秒後進入打卡流程。

🛠️ 新增：每月自動檢查 cookie 有效性
新增一個 check_cookie_start.bat 啟動檔案，用來檢查 login_state.json 是否即將過期。

排程器需額外建立一個新任務，指向 check_cookie_start.bat。

執行時間建議設定為：每月10日早上 9:00。

如果 cookie 有效，Telegram 會發出剩餘天數通知；如果即將失效，也會提醒更新。



✅ 完成這些設定後，clockin-bot即可穩定運作！
✅ 每天準時自動打卡，出錯時即時Telegram通知！

# 🚀 clockin-bot 正式啟動！