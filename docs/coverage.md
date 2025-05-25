# 🧪 測試覆蓋率與執行流程（Coverage & Test Instructions）

本專案採用 `pytest` 進行單元測試與整合測試，  
並整合 `pytest-cov` 收集測試覆蓋率，產出 HTML 報表供視覺化檢閱。

---

## ✅ 測試目標區分（Testing Strategy）

| 階段 | 說明 | 測試目錄 |
|------|------|----------|
| Unit Test | 測試單一模組功能是否正確（無依賴） | `test/unit/` |
| Integration Test | 模組組合是否正確運作（ex: controller） | `test/integration/` |
| E2E Test | 整體流程（VPN → 打卡 → 通知）是否成功 | `test/e2e/` |

---

## ✅ 如何執行完整測試流程（含覆蓋率）

請先啟動虛擬環境：

```bash
cd C:\Users\user\Desktop\104-autologin
venv\Scripts\activate
```

然後執行控制器：

```bash
python -m clockin_bot.test.run_ci_like_tests
```

---

## ✅ 自動產出測試覆蓋率報表（HTML 格式）

上述指令會同時產出測試覆蓋率報表，儲存在：

```
htmlcov/index.html
```

你可以直接用瀏覽器開啟該檔案：

```bash
start htmlcov\index.html  # Windows
open htmlcov/index.html   # macOS
```

---

## 📁 測試資料夾結構對照表

```
test/
├── unit/           ← 單元測試（功能模組）
├── integration/    ← 模組整合測試
├── e2e/            ← 主流程測試（等同正式執行流程）
├── run_ci_like_tests.py ← 本地版的 CI controller（模擬 GitHub Actions）
```

---

## 🧾 測試報表說明

| 檔案 | 說明 |
|------|------|
| `htmlcov/index.html` | 視覺化覆蓋率報表 |
| `pytestlog_YYYYMMDD_HHMM.log` | 本地測試執行結果 log，儲存於 `logs/` 目錄中 |

> ✅ 若不想推上 GitHub，請將 `htmlcov/` 與 `*.log` 加入 `.gitignore`

---

## 🎯 建議配套做法

- 將 `run_ci_like_tests.py` 加入 bat 腳本（例如 `scripts/run_tests.bat`）
- 在每次推送前手動跑一次，確認主流程與覆蓋率未退化
- 搭配 `docs/test_strategy.md` 說明測試設計理_

