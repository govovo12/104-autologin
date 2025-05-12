# Clockin-Bot 自動打卡系統

本專案自動化實現：
- 啟動 VPN (Outline)
- 智能 OCR 檢查 VPN 連線狀態
- 自動登入 104 打卡系統
- **打卡後透過 API 回應判斷是否成功**
- 檢查國定假日與自訂排除日，自動跳過
- 支援 Telegram 訊息推送通知

---

## 🛠 事前準備（首次安裝環境） 

1. **安裝 Python 3.8～3.12**
   - 官方網站：[https://www.python.org/](https://www.python.org/)
   - 安裝時記得勾選 `Add Python to PATH`！

2. **安裝 VSCode（選用，建議）**
   - 官方網站：[https://code.visualstudio.com/](https://code.visualstudio.com/)
   - 方便編輯 .py 和 .bat 檔案。

3. **安裝 Outline 桌面版**
   - 並確認有**`Outline.lnk`捷徑放在桌面**！

4. **準備 Telegram BOT Token 和 Chat ID**
   - 本專案支援打卡成功／失敗推送通知。

5. **特別提醒：第一次登入保存 Cookie 時請手動操作到「私人秘書」頁面並截圖備存**
   - 避免未來 cookie 效期或登入流程改版時無法比對問題。

---

## ⚡ 快速開始（Quick Start）

1. 下載專案並安裝虛擬環境
   ```bash
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. 安裝 Playwright 所需的瀏覽器（很重要！）
   ```bash
   playwright install
   ```

3. 手動儲存登入狀態
   ```bash
   python -m scripts.login_save_cookie
   ```
   ⚠️ 登入 104 統一入口網站，完成驗證、跳轉到「私人秘書」頁面後，按 Enter 保存 login_state.json。

4. 執行主程式（自動打卡）
   ```bash
   bat\clockin_start.bat
   ```

5. 檢查 Cookie 過期提醒
   ```bash
   bat\run_check_cookie.bat
   ```

6. 顯示專案資料夾結構
   ```bash
   bat\show_structure.bat
   ```

📦 資料夾結構

clockin-bot/
│
├── bat/                  # 各種啟動批次檔 (.bat)
├── data/                 # 登入資料與假日設定
├── scripts/              # 主要Python腳本
├── vpn_outline_connect/  # VPN操作與OCR圖片
├── requirements.txt      # 需要安裝的Python套件
├── README.md             # 使用說明（本文件）
├── .gitignore            # 忽略設定
└── print_clean_structure.py  # 顯示資料夾結構的小工具

---

## 🆕 版本變更紀錄（CHANGELOG）

🔵 Clockin-Bot v1.4（打卡邏輯更新）

🛠 **打卡流程升級：由原本透過畫面比對圖像判斷打卡成功，改為直接使用 API 回傳結果判斷**。

🛠 流程更穩定，新增失敗重試與精確回應印出，避免誤判與畫面問題。

🛠 其他邏輯與排程整合方式保持一致，無需額外修改。

📬 Telegram通知說明  
打卡成功/失敗、VPN連線錯誤，都會即時推送訊息到你的 Telegram 頻道。

請在 `scripts/config.py` 中設定你的 `TELEGRAM_BOT_TOKEN` 與 `TELEGRAM_CHAT_ID`。

📅 假日與手動排除設定  
`data/holidays_2025.json`：行政院公布之國定假日（自動判斷）

`data/manual_skip_days.json`：自訂要排除的特殊日期（可手動編輯）

⚙️ 其他注意事項
- 必須有 Outline 桌面捷徑 (Outline.lnk) 在桌面上。
- 打卡網址設定為：https://pro.104.com.tw/psc2?m=b&m=b,b,b
- Playwright自動化操作，請保持Chrome Driver與瀏覽器版本相容。
- 本專案為個人自動化練習用途，請勿用於非法或商業用途。









