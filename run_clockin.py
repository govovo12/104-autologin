import sys
import argparse
import importlib
from pathlib import Path
from clockin_bot.logger.safe_print import safe_print

# ✅ 補上這段，讓 Python 能找到 clockin_bot、tools、vpn 等模組
ROOT_DIR = Path(__file__).resolve().parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))


def find_module_by_filename(base_dir: Path, target_filename: str):
    for py_file in base_dir.rglob("*.py"):
        if py_file.stem == target_filename:
            relative_path = py_file.relative_to(base_dir.parent).with_suffix("")
            module_path = ".".join(relative_path.parts)
            return module_path
    return None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--task", required=True, help="模組檔名（例如 clockin_104）")
    parser.add_argument("--action", help="子控要執行的動作（例如 start / stop）")
    args = parser.parse_args()

    base_dir = Path(__file__).resolve().parent / "clockin_bot"
    module_path = find_module_by_filename(base_dir, args.task)
    print(f"[DEBUG] 找到模組路徑：{module_path}")
    
    if not module_path:
        safe_print(f"❌ 找不到符合名稱的模組：{args.task}.py")
        return

    try:
        task_module = importlib.import_module(module_path)

        if hasattr(task_module, "__task_info__"):
            task_meta = getattr(task_module, "__task_info__")
            entry = task_meta.get("entry")
            desc = task_meta.get("desc", "")
            if callable(entry):
                safe_print(f"✅ 執行 {module_path} 任務：{desc}")
                # 如果 entry 接受參數就傳 action，否則直接呼叫
                if args.action:
                    entry(args.action)
                else:
                    entry()
                return
            else:
                safe_print(f"⚠ 模組 {module_path} 的 __task_info__ 缺少有效 entry")
                return

        safe_print(f"⚠ 模組 {module_path} 沒有定義 __task_info__，請補上以支援新架構")

    except Exception as e:
        safe_print(f"❌ 模組執行錯誤：{e}")


if __name__ == "__main__":
    main()
