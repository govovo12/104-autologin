import json
from pathlib import Path

# 定位檔案路徑
BASE_DIR = Path(__file__).resolve().parent
data_dir = BASE_DIR / "clockin_bot" / "data"
login_state_path = data_dir / "login_state.json"
cookie_header_path = data_dir / "cookie_header.json"

# 讀取 login_state.json
try:
    with open(login_state_path, "r", encoding="utf-8") as f:
        login_state = json.load(f)
except FileNotFoundError:
    safe_print(f"❌ 找不到 login_state.json：{login_state_path}")
    exit(1)

# 解析 cookies
cookies = login_state.get("cookies", [])
if not cookies:
    safe_print("❌ login_state.json 中沒有 cookies 欄位")
    exit(1)

cookie_str = "; ".join(f"{c['name']}={c['value']}" for c in cookies)
cookie_header = {
    "cookie": cookie_str,
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
}

# 寫入 cookie_header.json
with open(cookie_header_path, "w", encoding="utf-8") as f:
    json.dump(cookie_header, f, ensure_ascii=False, indent=2)

safe_print(f"✅ 已成功產生 cookie_header.json：\n{cookie_header_path}")
