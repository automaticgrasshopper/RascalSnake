import turtle
import os
import sys
from save_manager import SaveManager
from score_display import ScoreDisplay
from save_manager import SaveManager
from score_display import ScoreDisplay
from scenes.title_scene import TitleScene
from scenes.snake_game import SnakeGame
from scenes.purple_ending import PurpleEnding
from scenes.blue_mode_intro import BlueModeIntro
from scenes.blue_breakout import BlueBreakout
from scenes.blue_plane import BluePlane
from scenes.blue_qte import BlueQTE
from scenes.red_ending import RedEnding
from scenes.red_star_verification import RedStarVerification
from scenes.red_snake_intro import RedSnakeIntro
from scenes.red_snake_game import RedSnakeGame
from scenes.red_breakout_intro import RedBreakoutIntro
from scenes.red_breakout import RedBreakout
from scenes.red_breakout_snake import RedBreakoutSnake  # 新增导入
from scenes.red_plane_intro import RedPlaneIntro
from scenes.red_plane import RedPlane
from scenes.red_qte_intro import RedQTEIntro
from scenes.red_qte import RedQTE
from scenes.normal_snake import NormalSnake
from constants import GameState, SCREEN_WIDTH, SCREEN_HEIGHT, BG_COLOR

class GameManager:
    def __init__(self):
        # 初始化屏幕...
        self.screen = turtle.Screen()
        self.screen.setup(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.screen.title("Rascal Snake")
        self.screen.bgcolor(BG_COLOR)
        self.screen.tracer(0)
        
        # === 新增：设置窗口图标 ===
        def resource_path(relative_path):
            """获取资源的绝对路径。用于打包后访问资源文件。"""
            if hasattr(sys, '_MEIPASS'):
                # 如果程序在打包后的临时文件夹中运行
                base_path = sys._MEIPASS
            else:
                # 如果程序在开发环境中运行
                base_path = os.path.abspath(".")
            return os.path.join(base_path, relative_path)
        
        # 获取图标的路径
        icon_path = resource_path("favicon.ico")
        
        try:
            # 获取turtle底层对应的tkinter窗口并设置图标
            root_window = self.screen.getcanvas().winfo_toplevel()
            root_window.iconbitmap(icon_path)  # 在Windows上设置窗口图标
            print(f"图标设置成功: {icon_path}")
        except Exception as e:
            print(f"图标设置失败: {e}")
            # 如果上面的方法失败，尝试其他方法
            try:
                # 另一种设置图标的方法
                self.screen._root.iconbitmap(icon_path)
            except:
                print("备用图标设置方法也失败")
        # === 图标设置结束 ===
        
        # 窗口关闭处理
        self.screen._root.protocol("WM_DELETE_WINDOW", self.on_window_close)
        
        # 游戏状态
        self.current_state = GameState.TITLE
        self.save_data = SaveManager.load_save()
        self.current_game_score = 0
        self.session_total_score = 0
        
        # 初始化所有场景
        self.title_scene = TitleScene(self)
        self.snake_game = SnakeGame(self)
        self.purple_ending = PurpleEnding(self)
        self.blue_mode_intro = BlueModeIntro(self)
        self.blue_breakout = BlueBreakout(self)
        self.blue_plane = BluePlane(self)
        self.blue_qte = BlueQTE(self)
        self.red_ending = RedEnding(self)
        self.red_star_verification = RedStarVerification(self)
        self.red_snake_intro = RedSnakeIntro(self)
        self.red_snake_game = RedSnakeGame(self)
        self.red_breakout_intro = RedBreakoutIntro(self)
        self.red_breakout = RedBreakout(self)
        self.red_breakout_snake = RedBreakoutSnake(self)  # 新增实例化
        self.red_plane_intro = RedPlaneIntro(self)
        self.red_plane = RedPlane(self)
        self.red_qte_intro = RedQTEIntro(self)
        self.red_qte = RedQTE(self)
        self.normal_snake = NormalSnake(self)
        
        # 分数显示
        self.score_display = ScoreDisplay(self)
        
        print("游戏管理器初始化完成")
        
    def on_window_close(self):
        """窗口关闭处理 - 修复：保存历史最高分"""
        print("游戏窗口关闭")
        # 保存当前历史最高分
        if self.session_total_score > self.save_data.historical_total:
            self.save_data.historical_total = self.session_total_score
            print(f"更新历史最高分: {self.save_data.historical_total}")
        SaveManager.save_game(self.save_data)
        self.screen.bye()
        
    def run(self):
        """运行游戏主循环"""
        try:
            print("开始游戏主循环")
            while True:
                try:
                    # 状态处理 - 补充所有缺失的状态
                    if self.current_state == GameState.TITLE:
                        self.title_scene.run()
                    elif self.current_state == GameState.SNAKE_GAME:
                        self.snake_game.run()
                    elif self.current_state == GameState.PURPLE_ENDING:
                        self.purple_ending.run()
                    elif self.current_state == GameState.BLUE_MODE:
                        self.blue_mode_intro.run()
                    elif self.current_state == GameState.BLUE_BREAKOUT:
                        self.blue_breakout.run()
                    elif self.current_state == GameState.BLUE_PLANE:
                        self.blue_plane.run()
                    elif self.current_state == GameState.BLUE_QTE:
                        self.blue_qte.run()
                    elif self.current_state == GameState.RED_ENDING:
                        self.red_ending.run()
                    elif self.current_state == GameState.RED_STAR_VERIFICATION:
                        self.red_star_verification.run()
                    elif self.current_state == GameState.RED_SNAKE_INTRO:
                        self.red_snake_intro.run()
                    elif self.current_state == GameState.RED_SNAKE:
                        self.red_snake_game.run()
                    elif self.current_state == GameState.RED_BREAKOUT_INTRO:
                        self.red_breakout_intro.run()
                    elif self.current_state == GameState.RED_BREAKOUT:
                        self.red_breakout.run()
                    elif self.current_state == GameState.RED_BREAKOUT_SNAKE:  # 新增状态处理
                        self.red_breakout_snake.run()
                    elif self.current_state == GameState.RED_PLANE_INTRO:
                        self.red_plane_intro.run()
                    elif self.current_state == GameState.RED_PLANE:
                        self.red_plane.run()
                    elif self.current_state == GameState.RED_QTE_INTRO:
                        self.red_qte_intro.run()
                    elif self.current_state == GameState.RED_QTE:
                        self.red_qte.run()
                    elif self.current_state == GameState.NORMAL_SNAKE:
                        self.normal_snake.run()
                    else:
                        print(f"未知状态: {self.current_state}")
                        self.change_state(GameState.TITLE)
                        
                except turtle.Terminator:
                    print("Turtle窗口关闭")
                    break
                except Exception as e:
                    print(f"游戏循环错误: {e}")
                    import traceback
                    traceback.print_exc()
                    SaveManager.log_error(f"游戏循环错误: {e}")
                    self.change_state(GameState.TITLE)
                    
        except Exception as e:
            print(f"致命错误: {e}")
            import traceback
            traceback.print_exc()
            SaveManager.log_error(f"致命错误: {e}")
            
    # 其他方法保持不变...
    def change_state(self, new_state, *args, **kwargs):
        """切换游戏状态，支持传递参数"""
        try:
            print(f"状态切换: {self.current_state} -> {new_state}")
            
            # 清除按键绑定
            self.screen.listen()
            for key in ["r", "R", "space", "Up", "Down", "Left", "Right", "a", "A", "s", "S", "d", "D", "f", "F", "j", "J", "k", "K", "l", "L", "Tab", "Return", "BackSpace"]:
                self.screen.onkeypress(None, key)
            
            # 重置当前游戏分数
            if new_state != self.current_state:
                self.reset_game_score()
            
            self.current_state = new_state
            
            # 特殊处理：红色打砖块蛇模式，传递前一个场景
            if new_state == GameState.RED_BREAKOUT_SNAKE and args:
                self.red_breakout_snake.run(args[0])
            elif new_state == GameState.RED_BREAKOUT_SNAKE:
                self.red_breakout_snake.run()
            
        except Exception as e:
            print(f"状态切换错误: {e}")
            SaveManager.log_error(f"状态切换错误: {e}")
        
    def clear_screen(self):
        """清除屏幕"""
        for turtle_obj in self.screen.turtles():
            if hasattr(self, 'score_display') and turtle_obj in self.score_display.turtles:
                continue
            turtle_obj.clear()
            turtle_obj.hideturtle()
        self.screen.clear()
        self.screen.bgcolor(BG_COLOR)
        
    def update_score_display(self):
        """更新分数显示"""
        if hasattr(self, 'score_display'):
            self.score_display.update()
        
    def add_score(self, points):
        """增加分数"""
        self.current_game_score += points
        self.session_total_score += points
        self.update_score_display()
        
    def reset_game_score(self):
        """重置当前游戏分数"""
        self.current_game_score = 0
        self.update_score_display()
        
    def restart_to_title(self):
        """回到标题"""
        self.reset_game_score()
        self.session_total_score = 0
        self.change_state(GameState.TITLE)