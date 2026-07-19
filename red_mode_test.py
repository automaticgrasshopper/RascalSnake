#!/usr/bin/env python3
import sys
import os
import time

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import turtle
from save_manager import SaveManager
from game_manager import GameManager
from constants import GameState

class RedModeTest:
    def __init__(self):
        # 初始化屏幕
        self.screen = turtle.Screen()
        self.screen.setup(800, 600)
        self.screen.title("Rascal Snake - 红色模式测试")
        self.screen.bgcolor("black")
        self.screen.tracer(0)  # 关闭自动更新，手动控制
        
        # 游戏管理器
        self.manager = GameManager()
        
        # 设置测试模式
        self.manager.save_data.red_mode_completed = True
        self.manager.save_data.red_form_completed = True
        
        # 性能优化：设置帧率控制
        self.target_fps = 60
        self.frame_delay = 1.0 / self.target_fps
        
        # 显示测试菜单
        self.show_test_menu()
        
    def show_test_menu(self):
        """显示测试菜单"""
        self.clear_screen()
        
        # 标题
        title = turtle.Turtle()
        title.hideturtle()
        title.penup()
        title.color("red")
        title.goto(0, 200)
        title.write("红色模式测试菜单", align="center", font=("Arial", 24, "bold"))
        
        # 测试选项
        options = [
            "1 - 红色六芒星验证",
            "2 - 红色贪吃蛇介绍", 
            "3 - 红色贪吃蛇游戏",
            "4 - 红色打砖块介绍",
            "5 - 红色打砖块游戏",
            "6 - 红色飞机介绍",
            "7 - 红色飞机游戏",
            "8 - 红色QTE介绍",
            "9 - 红色QTE游戏",
            "0 - 红色墓碑结局",
            "T - 返回标题(正常模式)",
            "R - 重置分数",
            "F - 帧率显示切换"
        ]
        
        # 显示选项
        option_turtle = turtle.Turtle()
        option_turtle.hideturtle()
        option_turtle.penup()
        option_turtle.color("white")
        
        for i, option in enumerate(options):
            option_turtle.goto(-200, 100 - i * 30)
            option_turtle.write(option, align="left", font=("Arial", 14, "normal"))
        
        # 当前分数显示
        score_turtle = turtle.Turtle()
        score_turtle.hideturtle()
        score_turtle.penup()
        score_turtle.color("yellow")
        score_turtle.goto(0, -250)
        score_turtle.write(f"当前分数: {self.manager.session_total_score} | 历史最高: {self.manager.save_data.historical_total}", 
                          align="center", font=("Arial", 12, "normal"))
        
        # 帧率显示
        self.fps_turtle = turtle.Turtle()
        self.fps_turtle.hideturtle()
        self.fps_turtle.penup()
        self.fps_turtle.color("cyan")
        self.fps_turtle.goto(350, 280)
        self.show_fps = False
        self.last_frame_time = time.time()
        self.frame_count = 0
        self.fps = 0
        
        self.screen.update()
        
        # 绑定测试按键
        self.bind_test_keys()
        
    def bind_test_keys(self):
        """绑定测试按键"""
        self.screen.listen()
        self.screen.onkeypress(self.test_red_star, "1")
        self.screen.onkeypress(self.test_red_snake_intro, "2")
        self.screen.onkeypress(self.test_red_snake, "3")
        self.screen.onkeypress(self.test_red_breakout_intro, "4")
        self.screen.onkeypress(self.test_red_breakout, "5")
        self.screen.onkeypress(self.test_red_plane_intro, "6")
        self.screen.onkeypress(self.test_red_plane, "7")
        self.screen.onkeypress(self.test_red_qte_intro, "8")
        self.screen.onkeypress(self.test_red_qte, "9")
        self.screen.onkeypress(self.test_red_ending, "0")
        self.screen.onkeypress(self.return_to_title, "t")
        self.screen.onkeypress(self.return_to_title, "T")
        self.screen.onkeypress(self.reset_score, "r")
        self.screen.onkeypress(self.reset_score, "R")
        self.screen.onkeypress(self.toggle_fps, "f")
        self.screen.onkeypress(self.toggle_fps, "F")
        
    def toggle_fps(self):
        """切换帧率显示"""
        self.show_fps = not self.show_fps
        if not self.show_fps:
            self.fps_turtle.clear()
        
    def update_fps(self):
        """更新帧率显示"""
        if not self.show_fps:
            return
            
        self.frame_count += 1
        current_time = time.time()
        if current_time - self.last_frame_time >= 1.0:
            self.fps = self.frame_count
            self.frame_count = 0
            self.last_frame_time = current_time
            
            self.fps_turtle.clear()
            self.fps_turtle.write(f"FPS: {self.fps}", align="right", font=("Arial", 12, "normal"))
        
    def clear_screen(self):
        """清除屏幕"""
        for turtle_obj in self.screen.turtles():
            turtle_obj.clear()
            turtle_obj.hideturtle()
        self.screen.clear()
        self.screen.bgcolor("black")
        
    def start_test(self, target_state):
        """开始测试"""
        print(f"开始测试: {target_state}")
        
        # 重置游戏管理器的状态
        self.manager.current_state = target_state
        self.manager.clear_screen()
        
        # 运行游戏循环
        self.run_game_loop()
        
    def run_game_loop(self):
        """运行游戏循环 - 修复性能问题"""
        try:
            last_time = time.time()
            
            while True:
                try:
                    current_time = time.time()
                    delta_time = current_time - last_time
                    
                    # 帧率控制 - 确保稳定的60FPS
                    if delta_time < self.frame_delay:
                        time.sleep(self.frame_delay - delta_time)
                    
                    last_time = time.time()
                    
                    # 状态处理
                    if self.manager.current_state == GameState.RED_STAR_VERIFICATION:
                        self.manager.red_star_verification.run()
                    elif self.manager.current_state == GameState.RED_SNAKE_INTRO:
                        self.manager.red_snake_intro.run()
                    elif self.manager.current_state == GameState.RED_SNAKE:
                        self.manager.red_snake_game.run()
                    elif self.manager.current_state == GameState.RED_BREAKOUT_INTRO:
                        self.manager.red_breakout_intro.run()
                    elif self.manager.current_state == GameState.RED_BREAKOUT:
                        self.manager.red_breakout.run()
                    elif self.manager.current_state == GameState.RED_PLANE_INTRO:
                        self.manager.red_plane_intro.run()
                    elif self.manager.current_state == GameState.RED_PLANE:
                        self.manager.red_plane.run()
                    elif self.manager.current_state == GameState.RED_QTE_INTRO:
                        self.manager.red_qte_intro.run()
                    elif self.manager.current_state == GameState.RED_QTE:
                        self.manager.red_qte.run()
                    elif self.manager.current_state == GameState.RED_ENDING:
                        self.manager.red_ending.run()
                    elif self.manager.current_state == GameState.TITLE:
                        # 返回测试菜单
                        self.show_test_menu()
                        break
                    else:
                        print(f"未知测试状态: {self.manager.current_state}")
                        self.manager.current_state = GameState.TITLE
                        self.show_test_menu()
                        break
                        
                    # 更新帧率显示
                    self.update_fps()
                    self.screen.update()
                        
                except turtle.Terminator:
                    print("Turtle窗口关闭")
                    break
                except Exception as e:
                    print(f"测试循环错误: {e}")
                    import traceback
                    traceback.print_exc()
                    self.manager.current_state = GameState.TITLE
                    self.show_test_menu()
                    break
                    
        except Exception as e:
            print(f"测试致命错误: {e}")
            import traceback
            traceback.print_exc()
            
    # 测试方法
    def test_red_star(self):
        self.start_test(GameState.RED_STAR_VERIFICATION)
        
    def test_red_snake_intro(self):
        self.start_test(GameState.RED_SNAKE_INTRO)
        
    def test_red_snake(self):
        # 设置一些分数以便测试
        self.manager.current_game_score = 300
        self.manager.session_total_score = 300
        self.start_test(GameState.RED_SNAKE)
        
    def test_red_breakout_intro(self):
        self.start_test(GameState.RED_BREAKOUT_INTRO)
        
    def test_red_breakout(self):
        self.start_test(GameState.RED_BREAKOUT)
        
    def test_red_plane_intro(self):
        self.start_test(GameState.RED_PLANE_INTRO)
        
    def test_red_plane(self):
        self.start_test(GameState.RED_PLANE)
        
    def test_red_qte_intro(self):
        self.start_test(GameState.RED_QTE_INTRO)
        
    def test_red_qte(self):
        self.start_test(GameState.RED_QTE)
        
    def test_red_ending(self):
        self.start_test(GameState.RED_ENDING)
        
    def return_to_title(self):
        """返回标题"""
        self.manager.current_state = GameState.TITLE
        self.show_test_menu()
        
    def reset_score(self):
        """重置分数"""
        self.manager.current_game_score = 0
        self.manager.session_total_score = 0
        self.show_test_menu()

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
    print("=== Rascal Snake 红色模式测试启动 ===")
    
    # 设置错误日志
    setup_error_logging()
    
    try:
        print(f"存档位置: {SaveManager.get_save_path()}")
        print(f"日志位置: {SaveManager.get_log_path()}")
        
        # 创建测试实例
        test = RedModeTest()
        
        # 运行测试菜单
        test.show_test_menu()
        
        # 保持程序运行 - 使用我们自己的循环而不是turtle.mainloop()
        try:
            last_time = time.time()
            while True:
                current_time = time.time()
                delta_time = current_time - last_time
                
                # 帧率控制
                if delta_time < test.frame_delay:
                    time.sleep(test.frame_delay - delta_time)
                
                last_time = time.time()
                
                # 更新帧率显示
                test.update_fps()
                test.screen.update()
                
        except KeyboardInterrupt:
            print("测试模式被用户中断")
        except Exception as e:
            print(f"测试模式错误: {e}")
            import traceback
            traceback.print_exc()
        
    except Exception as e:
        print(f"测试启动失败: {e}")
        import traceback
        traceback.print_exc()
        
        # 记录错误
        SaveManager.log_error(f"测试启动失败: {e}\n{traceback.format_exc()}")
        
        # 显示错误信息
        input("按回车键退出...")