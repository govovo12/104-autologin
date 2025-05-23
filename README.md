# 104 打卡自動化系統（Clockin-Bot）

🎯 **目的**：自動連接 VPN、登入 104、打卡、上傳紀錄報告、並透過 Telegram 傳送打卡狀態通知。

---

## 📁 專案結構

```
104-autologin/
├── clockin_bot/                  # 主程式模組
│   ├── clockin/                 # 打卡邏輯
│   ├── config/                  # 設定檔載入與環境變數
│   ├── data/                    # cookie、假日表等資料檔
│   ├── logger/                  # 統一 log 寫入模組
│   ├── logs/                    # ❌ 已移除（log 已集中於根目錄 logs/）
│   ├── modules/                # 流程控制模組（如主腳本）
│   ├── notify/                 # Telegram 通知模組
│   ├── scripts/                # bat 腳本（啟動任務用）
│   ├── session/                # cookie 儲存與檢查
│   ├── test/                   # 測試用模組
│   ├── tools/                  # 工具函式、排程、報告轉換等
│   └── vpn/                    # VPN 啟動與設定模組
├── docs/                       # HTML 報告發佈（供 GitHub Pages 使用）
├── logs/                       # ✅ 所有打卡與執行 log 寫入於此
├── run_clockin.py             # 任務入口點（指定 --task 啟動模組）
├── .env                       # 本地環境變數（含 TG Token 等）
├── requirements.txt           # 依賴套件列表
└── README.md                  # 專案說明文件
```

---

## 🚀 核心功能

- ✅ 支援打卡前自動啟動 VPN（Outline 或 Shadowsocks）
- ✅ 執行前自動判斷是否為假日或排除日
- ✅ 可重試最多 3 次打卡流程（避免網路或驗證延遲）
- ✅ 將打卡狀態與錯誤訊息傳送到 Telegram
- ✅ 自動產出 log 與 HTML 報告並推送至 GitHub Pages

---

## 🧱 架構特色

- 所有模組皆整合 `__task_info__`，統一管理與可由 `run_clockin.py` 執行
- logger 模組提供裝飾器與集中 log 檔輸出
- 所有打卡、VPN、cookie 等功能模組皆模組化、可獨立測試
- 路徑採用旗標式寫法，確保跨系統一致性與可部署性

---

## 📦 安裝方式

```bash
cd 104-autologin
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

---

## 🕹 執行方式

### 主控打卡流程（含假日判斷 + VPN + 打卡 + 上傳報告）
```bash
python run_clockin.py --task scheduler_main
```

### 檢查 cookie 有效期限
```bash
python run_clockin.py --task check_cookie_expiry
```

### 查看資料夾結構
```bash
python run_clockin.py --task print_clean_structure
```

---

## 📝 備註

- log 已統一集中於根目錄 logs/，不再有 clockin_bot/logs/
- 所有報告皆會轉成 HTML 存至 docs/ 目錄並推送至 GitHub Pages
- 預設已關閉 GitHub Actions 自動執行，僅本地排程或手動執行

---

👨‍💻 製作：@govovo12
📬 意見請透過 Telegram bot 傳送
