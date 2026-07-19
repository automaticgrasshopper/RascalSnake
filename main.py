#!/usr/bin/env python3
import sys
import os

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from save_manager import SaveManager

def setup_error_logging():
    """设置错误日志"""
    SaveManager.ensure_save_dir()
    try:
        # 重定向stderr到日志文件
        log_path = SaveManager.get_log_path()
        sys.stderr = open(log_path, 'w', encoding='utf-8')
    except Exception as e:
        print(f"设置错误日志失败: {e}")

if __name__ == "__main__":
    print("=== Rascal Snake 游戏启动 ===")
    
    # 设置错误日志
    setup_error_logging()
    
    try:
        from game_manager import GameManager
        
        print(f"存档位置: {SaveManager.get_save_path()}")
        print(f"日志位置: {SaveManager.get_log_path()}")
        
        # 创建游戏实例并运行
        game = GameManager()
        game.run()
        
    except Exception as e:
        print(f"游戏启动失败: {e}")
        import traceback
        traceback.print_exc()
        
        # 记录错误
        SaveManager.log_error(f"游戏启动失败: {e}\n{traceback.format_exc()}")
        
        # 显示错误信息
        input("按回车键退出...")