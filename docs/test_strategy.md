# 🧪 測試策略說明（Test Strategy）

---

## 🎯 測試設計目標

- 確保每個模組邏輯能單獨驗證（unit test）
- 整合模組能正確協作（integration test）
- 主流程能從頭到尾穩定執行（e2e test）
- 所有打卡流程皆可重試與錯誤通知
- 模組應能適應 104 結構異動，快速定位問題來源（非 VPN / cookie）

---

## 🔧 測試類型區分

| 測試類型 | 目的 | 目錄 |
|----------|------|------|
| Unit Test | 驗證獨立模組行為（無副作用） | `test/unit/` |
| Integration Test | 模組間流程與回傳值是否正確 | `test/integration/` |
| E2E Test | VPN + 打卡 + 通知整合流程是否穩定 | `test/e2e/` |

---

## 🔄 Retry 設計說明

- 所有主流程與打卡皆使用 `run_with_retry` 裝飾器
- 預設重試 3 次，每次延遲 1 秒
- 錯誤會自動推送 Telegram，方便遠端監控

---

## 📦 測試覆蓋策略

- 每個模組建立對應測試檔案
- 對主要流程包含：
  - VPN 啟動是否成功
  - cookie 是否過期 / 不合法
  - API 回傳是否符合預期格式
  - 成功與失敗推播皆能觸發
- 未 mock 外部 API，但可擴充

---

## ❗ 邊界條件與防呆驗證

- cookie 失效、VPN 未啟動、response 非 200、message 為 Unauthorized
- 手動略過日、假日自動跳過
- 確保 log 寫入與路徑合法性

---

## ✅ 未來測試可擴充方向

- mock Telegram 推播，避免實際送出
- 引入 pytest-mark 動態切分
- 將 cookie 測試改為 fake api 測資
