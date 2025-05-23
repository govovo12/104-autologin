import sys
from pathlib import Path
import importlib.util
import traceback

# 加入專案根目錄
BASE_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(BASE_DIR))

def find_all_py_files(base_path):
    return [p for p in base_path.rglob("*.py") if not p.name.startswith("__")]

def import_module_from_path(py_path):
    try:
        relative_path = py_path.relative_to(BASE_DIR).with_suffix("")
        module_name = ".".join(relative_path.parts)
        spec = importlib.util.spec_from_file_location(module_name, py_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module_name, module
    except Exception:
        return None, None

def find_tasks():
    task_modules = []
    for py_file in find_all_py_files(BASE_DIR / "clockin_bot"):
        module_name, module = import_module_from_path(py_file)
        if not module:
            continue
        if hasattr(module, "__task_info__"):
            info = module.__task_info__
            task_name = info.get("name", "(無名稱)")
            desc = info.get("desc", "(無描述)")
            entry = info.get("entry")
            entry_name = entry.__name__ if callable(entry) else "(無入口)"
            task_modules.append((task_name, desc, entry_name, module_name))
    return task_modules

def print_tasks(tasks):
    if not tasks:
        print("❌ 沒有找到任何 __task_info__ 註冊的模組")
        return

    print("✅ 已註冊任務清單：\n")
    for name, desc, entry, mod in tasks:
        print(f"- {name.ljust(20)} → {desc}")
        print(f"  🔹 module: {mod}")
        print(f"  🔹 entry : {entry}\n")

if __name__ == "__main__":
    print_tasks(find_tasks())
