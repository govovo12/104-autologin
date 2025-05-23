import subprocess
from datetime import datetime
from pathlib import Path
from shutil import copyfile

def upload_log_only():
    base_dir = Path(__file__).resolve().parent.parent.parent  # 專案根目錄
    log_src = base_dir / "logs" / "latest_log_view.html"
    log_dest = base_dir / "docs" / "latest_log_view.html"

    if not log_src.exists():
        print("❌ 找不到報告檔 logs/latest_log_view.html")
        return

    # 確保 docs/ 存在
    log_dest.parent.mkdir(parents=True, exist_ok=True)

    # 複製報告
    copyfile(log_src, log_dest)
    print(f"✅ 已複製報告到 docs/{log_dest.name}")

    # 加入 staged 區域
    subprocess.run(["git", "add", str(log_dest)], check=True)

    # ✅ 檢查是否真的有東西被加入 staged
    check_status = subprocess.run(["git", "diff", "--cached", "--quiet"])
    if check_status.returncode == 0:
        print("⚠️ 沒有任何變更加入暫存區，跳過 commit。")
        return

    # Git commit + push
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        subprocess.run(["git", "commit", "-m", f"📄 更新報告 {timestamp}"], check=True)
        subprocess.run(["git", "push"], check=True)
        print("✅ 已推送報告至 GitHub Pages")
    except subprocess.CalledProcessError as e:
        print(f"❌ Git 操作失敗：{e}")

if __name__ == "__main__":
    upload_log_only()
