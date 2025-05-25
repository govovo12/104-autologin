from pathlib import Path
from clockin_bot.logger.safe_print import safe_print
EXCLUDE = {"venv", "__pycache__", ".git", ".idea", ".vscode"}

def print_structure(base: Path, prefix=""):
    for item in sorted(base.iterdir()):
        if item.name in EXCLUDE:
            continue
        if item.is_dir():
            safe_print(f"{prefix}📁 {item.name}/")
            print_structure(item, prefix + "    ")
        else:
            safe_print(f"{prefix}📄 {item.name}")

def run_print_structure():
    root = Path(__file__).resolve().parent.parent
    safe_print(f"📦 資料夾結構（排除 {', '.join(EXCLUDE)}）")
    print_structure(root)
    input("\n📌 請按任意鍵關閉視窗...")  # 防止 bat 閃退

__task_info__ = {
    "name": "print_structure",
    "desc": "列印專案資料夾結構（排除常見雜項）",
    "entry": run_print_structure,
}
