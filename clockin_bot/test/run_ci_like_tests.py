import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path
from clockin_bot.logger.safe_print import safe_print

# === 設定 log 檔案 ===
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

# 清除舊的 pytestlog_ 開頭的 log，只保留最新一次
for old_log in LOG_DIR.glob("pytestlog_*.log"):
    old_log.unlink()

# 建立新的 log 檔案名稱（含 timestamp）
timestamp = datetime.now().strftime("%Y%m%d_%H%M")
log_path = LOG_DIR / f"pytestlog_{timestamp}.log"

def write_log(message: str):
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(message + "\n")

# === 單階段測試執行 ===
def run_stage(name, folder):
    safe_print(f"\n🧪 Running {name} tests...")
    write_log(f"\n🧪 Running {name} tests...")

    start = time.time()
    result = subprocess.run(["pytest", folder, "-s"], capture_output=True, text=True)
    elapsed = time.time() - start

    if result.stdout:
        write_log(result.stdout)
    if result.stderr:
        write_log(result.stderr)

    if result.returncode != 0:
        msg = f"❌ {name} tests failed in {elapsed:.2f}s. Aborting CI-like flow."
        safe_print(msg)
        write_log(msg)
        sys.exit(result.returncode)

    msg = f"✅ {name} tests passed in {elapsed:.2f}s."
    safe_print(msg)
    write_log(msg)

# === 覆蓋率階段 ===
def run_coverage():
    safe_print("\n🧪 Running Coverage Report...")
    write_log("\n🧪 Running Coverage Report...")

    result = subprocess.run([
        "pytest",
        "--cov=clockin_bot",
        "--cov-report=term-missing",
        "--cov-report=html"
    ], capture_output=True, text=True)

    if result.stdout:
        write_log(result.stdout)
    if result.stderr:
        write_log(result.stderr)

    if result.returncode != 0:
        msg = "❌ Coverage collection failed."
        safe_print(msg)
        write_log(msg)
        sys.exit(result.returncode)

    msg = "✅ Coverage report generated. (HTML: htmlcov/index.html)"
    safe_print(msg)
    write_log(msg)

# === 主流程 ===
def main():
    run_stage("Unit", "clockin_bot/test/unit")
    run_stage("Integration", "clockin_bot/test/integration")
    run_stage("E2E", "clockin_bot/test/e2e")
    run_coverage()

    final_msg = "\n✅ All test stages + coverage passed successfully."
    safe_print(final_msg)
    write_log(final_msg)

if __name__ == "__main__":
    main()
