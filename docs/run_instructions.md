# 🚀 執行方式說明（Run Instructions）

本文件說明如何執行本專案中所有可用的任務模組，包括：

- 如何透過 `.bat` 執行（免安裝指令）
- 如何透過 CLI 執行 `run_clockin.py --task 任務名`
- 任務名稱從哪裡查詢

---

## ✅ 方法一：使用 `.bat` 快捷指令（推薦給非工程師）

### 📂 進入 `scripts/` 資料夾，點擊以下檔案：

| 檔名 | 功能 |
|------|------|
| `list_tasks.bat` | 顯示目前所有可執行任務與描述 |
| `run_task.bat` | 手動輸入任務名稱並執行該任務 |
| `run_main.bat` | 直接執行打卡主流程（可自定義內容） |
| `run_structure.bat` | 顯示專案的乾淨目錄結構（用於調試或部署） |

---

### 🖥 使用範例（點兩下 `run_task.bat`）：

```
請輸入要執行的任務名稱（例如 clockin_104）：
scheduler_main
```

執行完成後會自動顯示 log、執行狀態，並可整合 Telegram 推播通知。

---

## ✅ 方法二：使用 Python CLI 指令（進階用戶）

確保你已進入虛擬環境：

```bash
cd C:\Users\user\Desktop\104-autologin
venv\Scripts\activate
```

執行指定任務：

```bash
python run_clockin.py --task 任務名稱
```

範例：

```bash
python run_clockin.py --task clockin_104
python run_clockin.py --task login_and_convert_cookie
python run_clockin.py --task scheduler_main
```

---

## 🔍 如何查詢有哪些任務？

你可以執行以下任一方式列出所有任務清單：

```bash
# CLI 方式
python -m clockin_bot.tools.list_tasks

# 或使用 .bat
scripts\list_tasks.bat
```

執行結果會顯示如下：

```
🔸 可執行任務：
- clockin_104 → 發送打卡 API
- check_cookie_expiry_v2 → 檢查 cookie 是否過期
- ...
```

---

## 🧠 小提醒

- 所有任務模組皆透過 `__task_info__` 自動註冊，無需硬編路徑
- `.bat` 與 `run_clockin.py` 都共用這套任務系統，請善用
- 模組皆有 log 與錯誤回傳，請查看 logs/ 資料夾

---

✅ 建議搭配 `docs/tasks_list.md` 查看所有任務說明  
✅ 若需測試與覆蓋率驗證，請見 `docs/coverage.md`
