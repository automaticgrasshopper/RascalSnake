import os
import json
from save_manager import SaveManager

def check_save_files():
    """检查存档和日志文件状态"""
    print("=== Rascal Snake 文件检查 ===")
    
    # 检查保存目录
    if os.path.exists(SaveManager.SAVE_DIR):
        print(f"✓ 保存目录存在: {SaveManager.SAVE_DIR}")
    else:
        print(f"✗ 保存目录不存在: {SaveManager.SAVE_DIR}")
        return
    
    # 检查存档文件
    if os.path.exists(SaveManager.SAVE_FILE):
        print(f"✓ 存档文件存在: {SaveManager.SAVE_FILE}")
        try:
            with open(SaveManager.SAVE_FILE, 'r', encoding='utf-8') as f:
                save_data = json.load(f)
            print("存档内容:")
            for key, value in save_data.items():
                print(f"  {key}: {value}")
        except Exception as e:
            print(f"✗ 读取存档文件失败: {e}")
    else:
        print(f"✗ 存档文件不存在: {SaveManager.SAVE_FILE}")
    
    # 检查日志文件
    if os.path.exists(SaveManager.LOG_FILE):
        print(f"✓ 日志文件存在: {SaveManager.LOG_FILE}")
        file_size = os.path.getsize(SaveManager.LOG_FILE)
        print(f"日志文件大小: {file_size} 字节")
        
        if file_size > 0:
            print("最近日志内容:")
            try:
                with open(SaveManager.LOG_FILE, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    # 显示最后10行
                    for line in lines[-10:]:
                        print(f"  {line.strip()}")
            except Exception as e:
                print(f"✗ 读取日志文件失败: {e}")
        else:
            print("日志文件为空")
    else:
        print(f"✗ 日志文件不存在: {SaveManager.LOG_FILE}")

if __name__ == "__main__":
    check_save_files()
    
    input("\n按回车键退出...")