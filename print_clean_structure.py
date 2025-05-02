import os

EXCLUDED_DIRS = {"venv", "__pycache__", ".git", ".pytest_cache"}
ROOT_DIR = "."

def list_structure(base_path, indent=""):
    for item in sorted(os.listdir(base_path)):
        if item in EXCLUDED_DIRS:
            continue
        full_path = os.path.join(base_path, item)
        print(f"{indent}{item}/" if os.path.isdir(full_path) else f"{indent}{item}")
        if os.path.isdir(full_path):
            list_structure(full_path, indent + "    ")

if __name__ == "__main__":
    print("=== Clockin-Bot 專案結構清單（已排除無用資料夾）===\n")
    list_structure(ROOT_DIR)
