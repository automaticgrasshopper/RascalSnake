import json
import os

class SaveData:
    def __init__(self):
        self.purple_completed = False
        self.blue_completed = False
        self.red_form_completed = False
        self.red_mode_completed = False
        self.historical_total = 0
        
    def to_dict(self):
        return {
            'purple_completed': self.purple_completed,
            'blue_completed': self.blue_completed,
            'red_form_completed': self.red_form_completed,
            'red_mode_completed': self.red_mode_completed,
            'historical_total': self.historical_total
        }
    
    def from_dict(self, data):
        self.purple_completed = data.get('purple_completed', False)
        self.blue_completed = data.get('blue_completed', False)
        self.red_form_completed = data.get('red_form_completed', False)
        self.red_mode_completed = data.get('red_mode_completed', False)
        self.historical_total = data.get('historical_total', 0)

class SaveManager:
    SAVE_DIR = "save"
    SAVE_FILE = "rascal_snake_save.json"
    LOG_FILE = "error_log.txt"
    
    @staticmethod
    def get_save_path():
        return os.path.join(SaveManager.SAVE_DIR, SaveManager.SAVE_FILE)
    
    @staticmethod
    def get_log_path():
        return os.path.join(SaveManager.SAVE_DIR, SaveManager.LOG_FILE)
    
    @staticmethod
    def ensure_save_dir():
        """确保保存目录存在"""
        if not os.path.exists(SaveManager.SAVE_DIR):
            os.makedirs(SaveManager.SAVE_DIR)
            print(f"创建保存目录: {SaveManager.SAVE_DIR}")
    
    @staticmethod
    def load_save():
        """加载存档"""
        SaveManager.ensure_save_dir()
        save_data = SaveData()
        try:
            save_path = SaveManager.get_save_path()
            if os.path.exists(save_path):
                with open(save_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    save_data.from_dict(data)
                print(f"存档已加载: {save_path}")
            else:
                print("创建新存档")
        except Exception as e:
            print(f"加载存档错误: {e}")
            SaveManager.log_error(f"加载存档错误: {e}")
        return save_data
    
    @staticmethod
    def save_game(save_data):
        """保存游戏"""
        SaveManager.ensure_save_dir()
        try:
            save_path = SaveManager.get_save_path()
            with open(save_path, 'w', encoding='utf-8') as f:
                json.dump(save_data.to_dict(), f, indent=2)
            print(f"游戏已保存: {save_path}")
        except Exception as e:
            print(f"保存游戏错误: {e}")
            SaveManager.log_error(f"保存游戏错误: {e}")
    
    @staticmethod
    def log_error(error_message):
        """记录错误日志"""
        SaveManager.ensure_save_dir()
        try:
            log_path = SaveManager.get_log_path()
            with open(log_path, 'a', encoding='utf-8') as f:
                import datetime
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                f.write(f"[{timestamp}] {error_message}\n")
        except Exception as e:
            print(f"写入日志错误: {e}")