✅ 新版 README.md（v2.0 架構）
markdown

# Clockin-Bot 自動打卡系統 v2.0

本專案實現「跨平台、自動化、無 GUI 依賴」的 104 打卡流程，並整合 VPN 控制、API 驗證、Log 記錄、Telegram 通知與雲端部署能力。

---

## ✅ 功能簡介

- 📡 自動透過 SOCKS5 VPN 連線（支援 Outline 金鑰轉換）
- ✅ 透過 API 判斷打卡成功與否（不再依賴畫面比對）
- 📅 自動判斷國定假日與自訂排除日，自動跳過
- 🔁 打卡失敗自動重試三次，並推送 Telegram 通知
- 📄 打卡 log 自動儲存、可上傳至 GitHub Pages 檢視
- 💬 支援每日打卡摘要推送至 Telegram

---

## ⚙️ 安裝與執行步驟（本地端）

### 1. 建立虛擬環境與安裝套件

```bash
python -m venv venv
venv\Scripts\activate         # Windows
# source venv/bin/activate    # Linux/macOS
pip install -r requirements.txt
2. 安裝 Playwright 瀏覽器（首次執行）

playwright install
3. 建立 .env 檔案設定 Telegram 參數
env

TELEGRAM_BOT_TOKEN=xxx
TELEGRAM_CHAT_ID=xxx
你也可以參考 .env.example 範本。

🕹 使用方式
🔐 儲存 Cookie（只需做一次）

python run_login_save_cookie.py
會自動打開瀏覽器，登入 104 並儲存 login_state.json

⏰ 執行打卡流程

python run_clockin.py
支援自動判斷是否為假日、自動連線 VPN、自動登入與打卡、失敗自動重試與通知。

🧾 專案資料結構

clockin-bot/
├── run_clockin.py                 # 主程式入口
├── requirements.txt              # 套件清單
├── .env.example                  # 環境變數範例
├── clockin/                      # 打卡邏輯模組
├── config/                       # 全域參數、登入路徑設定
├── data/                         # 假日設定與 cookie 存檔
├── logger/                       # 日誌紀錄與裝飾器
├── logs/                         # log 檔輸出路徑
├── modules/scheduler/            # 排程控制流程
├── notify/                       # Telegram 推播模組
├── session/                      # Cookie 儲存與檢查邏輯
├── tools/                        # 時間/延遲/假日工具模組
├── vpn/                          # VPN 控制與 ss-local 配置
└── .gitignore                    # 忽略項目
📌 注意事項
登入流程需先手動完成一次登入並儲存 cookie（可用 30～90 天）

VPN 現已全面改為使用 ss-local 並支援 Outline 金鑰轉換為 config

程式以 UTC+8（台北時間）為基準處理所有打卡與日誌記錄

🚧 TODO（v2.1 目標）
✅ log 自動上傳至 GitHub Pages

✅ Telegram 附上 log 超連結

⏳ 自動續期 login_state cookie

⏳ VM 專用啟動腳本／GitHub Actions CI 整合

🧑‍💻 聲明
本專案僅供自動化學習用途，請勿用於非法或濫用場景。104 為第三方平台，其政策與架構若有更動，本專案將不保證正常運行。