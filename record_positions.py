import pyautogui
import time

# 要記錄的項目
items = [
    "Outline左上角",
    "連線按鈕左上角",
    "連線按鈕右下角",
    "已連線左上角",
    "已連線右下角"
]

recorded_positions = {}

print("🖱️ 自動座標記錄器啟動！")
print("請依提示，將滑鼠移到指定位置，然後『按 Enter』直接記錄。")

for item in items:
    input(f"\n🔔 請將滑鼠移到【{item}】，然後按 Enter 進行記錄...")

    # 直接記錄當前滑鼠位置
    x, y = pyautogui.position()
    recorded_positions[item] = (x, y)
    print(f"✅ 已記錄 {item}：X={x}, Y={y}")

# --- 全部記錄完成後 ---

print("\n📋 座標記錄完成！以下是全部結果：\n")
print(f"{'項目':<20}{'X座標':<10}{'Y座標':<10}")
print("-" * 40)
for item, (x, y) in recorded_positions.items():
    print(f"{item:<20}{x:<10}{y:<10}")

print("\n✅ 所有位置都已記錄完畢！可以複製保存了。")
