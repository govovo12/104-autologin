# 🧩 任務清單總覽（Task Registry Overview）

本專案透過 `__task_info__` 機制，統一註冊可執行模組，讓每一項功能都可透過 `run_clockin.py --task xxx` 或 `run_task.bat` 呼叫。

以下是目前已註冊的所有任務模組與功能說明：

---

## ✅ 打卡相關模組

| 任務名稱 | 描述 |
|----------|------|
| `clockin_104` | 發送 requests API 進行 104 打卡，成功推播 Telegram |
| `check_cookie_expiry_v2` | 檢查 login_state.json 內最晚過期 cookie 的狀態與分類 |
| `convert_login_cookie` | 將 login_state.json 轉換為 cookie_header.json（只抓 pro.104.com.tw） |
| `login_save_cookie` | 開啟 104 網頁，登入後儲存登入狀態到 login_state.json（需手動按 Enter） |
| `login_and_convert_cookie` | 一條龍流程：登入後自動轉換 cookie header 並儲存結果 |

---

## 🧠 工具／輔助模組

| 任務名稱 | 描述 |
|----------|------|
| `list_tasks` | 顯示所有 `__task_info__` 註冊任務模組與說明 |
| `print_clean_structure` | 印出目前專案目錄結構（已排除 .git, __pycache__ 等雜訊） |

---

## 🚀 主流程模組

| 任務名稱 | 描述 |
|----------|------|
| `scheduler_main` | 主流程控制器：判斷假日 → 啟動 VPN → 執行打卡 → 推播結果（含 retry） |

---

## 💡 使用方式範例

## 或使用 .bat 快捷工具：
scripts\list_tasks.bat      ← 顯示所有任務
scripts\run_task.bat        ← 輸入任務名稱並執行

📝 本清單會隨著模組新增或移除而更新，請搭配實際 __task_info__ 註冊狀態為準。





