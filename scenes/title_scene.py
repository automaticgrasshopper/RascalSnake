import turtle
import time
from scenes.base_scene import BaseScene
from constants import GameState

class TitleScene(BaseScene):
    def __init__(self, game_manager):
        super().__init__(game_manager)
        self.title_art = None
        
    def create_title_art(self):
        self.title_art = turtle.Turtle()
        self.title_art.hideturtle()
        self.title_art.penup()
        
        # 检查完成状态
        red_completed = self.manager.save_data.red_mode_completed
        blue_completed = self.manager.save_data.blue_completed
        purple_completed = self.manager.save_data.purple_completed
        
        # 根据完成状态确定颜色组合
        if red_completed and blue_completed and purple_completed:
            # 所有模式完成：紫色字，蓝色外圈，红色边缘
            self.create_advanced_title("purple", "blue", "red")
        elif blue_completed and purple_completed:
            # 蓝色和紫色完成：紫色字，蓝色外圈
            self.create_advanced_title("purple", "blue")
        elif red_completed:
            # 红色模式完成：红色字
            self.create_simple_title("red")
        elif blue_completed:
            # 蓝色模式完成：蓝色字
            self.create_simple_title("blue")
        elif purple_completed:
            # 紫色模式完成：紫色字
            self.create_simple_title("purple")
        else:
            # 未完成任何模式：白色文字
            self.create_simple_title("white")
            
    def create_simple_title(self, color):
        """创建简单标题（无特效）"""
        self.title_art.color(color)
        self.title_art.goto(0, 100)
        
        # ASCII艺术字标题 - Rascal Snake
        ascii_art = [
            "▓▓▓▓▓▓▓▓▓▓  ▓▓▓▓▓▓▓   ▓▓▓▓▓▓▓▓▓▓▓▓  ▓▓▓▓▓▓▓▓▓▓  ▓▓▓▓▓▓▓   ▓▓▓▓▓▓▓▓",
            "▓▓▓▓▓▓▓▓▓▓ ▓▓▓▓▓▓▓▓▓  ▓▓▓▓▓▓▓▓▓▓▓▓ ▓▓▓▓▓▓▓▓▓▓▓ ▓▓▓▓▓▓▓▓▓ ▓▓▓▓▓▓▓▓",
            "▓▓▓▓       ▓▓▓▓ ▓▓▓▓▓     ▓▓▓▓     ▓▓▓▓   ▓▓▓▓ ▓▓▓▓ ▓▓▓▓▓   ▓▓▓▓  ",
            "▓▓▓▓▓▓▓▓   ▓▓▓▓  ▓▓▓▓     ▓▓▓▓     ▓▓▓▓▓▓▓▓▓▓▓ ▓▓▓▓  ▓▓▓▓   ▓▓▓▓  ",
            "▓▓▓▓       ▓▓▓▓   ▓▓▓     ▓▓▓▓     ▓▓▓▓   ▓▓▓▓ ▓▓▓▓   ▓▓▓   ▓▓▓▓  ",
            "▓▓▓▓       ▓▓▓▓    ▓▓▓    ▓▓▓▓     ▓▓▓▓   ▓▓▓▓ ▓▓▓▓    ▓▓▓  ▓▓▓▓  "
        ]
        
        for i, line in enumerate(ascii_art):
            self.title_art.goto(-350, 150 - i * 30)
            self.title_art.write(line, align="left", font=("Courier", 10, "bold"))
            
        # 副标题
        subtitle = turtle.Turtle()
        subtitle.hideturtle()
        subtitle.penup()
        subtitle.color("white")
        subtitle.goto(0, -80)
        subtitle.write("Rascal Snake", align="center", font=("Arial", 20, "bold"))
        
        # 开始提示
        prompt = turtle.Turtle()
        prompt.hideturtle()
        prompt.penup()
        prompt.color("yellow")
        prompt.goto(0, -150)
        prompt.write("Press SPACE to start", align="center", font=("Arial", 16, "normal"))
        
    def create_advanced_title(self, base_color, *effect_colors):
        """创建带特效的标题"""
        # 先绘制特效层（描边）
        for effect_color in effect_colors:
            effect_turtle = turtle.Turtle()
            effect_turtle.hideturtle()
            effect_turtle.penup()
            effect_turtle.color(effect_color)
            effect_turtle.goto(0, 100)
            
            ascii_art = [
                "▓▓▓▓▓▓▓▓▓▓  ▓▓▓▓▓▓▓   ▓▓▓▓▓▓▓▓▓▓▓▓  ▓▓▓▓▓▓▓▓▓▓  ▓▓▓▓▓▓▓   ▓▓▓▓▓▓▓▓",
                "▓▓▓▓▓▓▓▓▓▓ ▓▓▓▓▓▓▓▓▓  ▓▓▓▓▓▓▓▓▓▓▓▓ ▓▓▓▓▓▓▓▓▓▓▓ ▓▓▓▓▓▓▓▓▓ ▓▓▓▓▓▓▓▓",
                "▓▓▓▓       ▓▓▓▓ ▓▓▓▓▓     ▓▓▓▓     ▓▓▓▓   ▓▓▓▓ ▓▓▓▓ ▓▓▓▓▓   ▓▓▓▓  ",
                "▓▓▓▓▓▓▓▓   ▓▓▓▓  ▓▓▓▓     ▓▓▓▓     ▓▓▓▓▓▓▓▓▓▓▓ ▓▓▓▓  ▓▓▓▓   ▓▓▓▓  ",
                "▓▓▓▓       ▓▓▓▓   ▓▓▓     ▓▓▓▓     ▓▓▓▓   ▓▓▓▓ ▓▓▓▓   ▓▓▓   ▓▓▓▓  ",
                "▓▓▓▓       ▓▓▓▓    ▓▓▓    ▓▓▓▓     ▓▓▓▓   ▓▓▓▓ ▓▓▓▓    ▓▓▓  ▓▓▓▓  "
            ]
            
            # 绘制偏移的特效层（模拟描边）
            offsets = [(-2, -2), (-2, 2), (2, -2), (2, 2)]
            for offset_x, offset_y in offsets:
                for i, line in enumerate(ascii_art):
                    effect_turtle.goto(-350 + offset_x, 150 - i * 30 + offset_y)
                    effect_turtle.write(line, align="left", font=("Courier", 10, "bold"))
        
        # 再绘制基础颜色层
        self.title_art.color(base_color)
        self.title_art.goto(0, 100)
        
        ascii_art = [
            "▓▓▓▓▓▓▓▓▓▓  ▓▓▓▓▓▓▓   ▓▓▓▓▓▓▓▓▓▓▓▓  ▓▓▓▓▓▓▓▓▓▓  ▓▓▓▓▓▓▓   ▓▓▓▓▓▓▓▓",
            "▓▓▓▓▓▓▓▓▓▓ ▓▓▓▓▓▓▓▓▓  ▓▓▓▓▓▓▓▓▓▓▓▓ ▓▓▓▓▓▓▓▓▓▓▓ ▓▓▓▓▓▓▓▓▓ ▓▓▓▓▓▓▓▓",
            "▓▓▓▓       ▓▓▓▓ ▓▓▓▓▓     ▓▓▓▓     ▓▓▓▓   ▓▓▓▓ ▓▓▓▓ ▓▓▓▓▓   ▓▓▓▓  ",
            "▓▓▓▓▓▓▓▓   ▓▓▓▓  ▓▓▓▓     ▓▓▓▓     ▓▓▓▓▓▓▓▓▓▓▓ ▓▓▓▓  ▓▓▓▓   ▓▓▓▓  ",
            "▓▓▓▓       ▓▓▓▓   ▓▓▓     ▓▓▓▓     ▓▓▓▓   ▓▓▓▓ ▓▓▓▓   ▓▓▓   ▓▓▓▓  ",
            "▓▓▓▓       ▓▓▓▓    ▓▓▓    ▓▓▓▓     ▓▓▓▓   ▓▓▓▓ ▓▓▓▓    ▓▓▓  ▓▓▓▓  "
        ]
        
        for i, line in enumerate(ascii_art):
            self.title_art.goto(-350, 150 - i * 30)
            self.title_art.write(line, align="left", font=("Courier", 10, "bold"))
            
        # 副标题
        subtitle = turtle.Turtle()
        subtitle.hideturtle()
        subtitle.penup()
        subtitle.color("white")
        subtitle.goto(0, -80)
        subtitle.write("Rascal Snake", align="center", font=("Arial", 20, "bold"))
        
        # 开始提示
        prompt = turtle.Turtle()
        prompt.hideturtle()
        prompt.penup()
        prompt.color("yellow")
        prompt.goto(0, -150)
        prompt.write("Press SPACE to start", align="center", font=("Arial", 16, "normal"))
        
    def show_normal_mode_unlocked(self):
        """显示普通模式已解锁的提示"""
        unlocked = turtle.Turtle()
        unlocked.hideturtle()
        unlocked.penup()
        unlocked.color("cyan")
        unlocked.goto(0, -200)
        unlocked.write("✓ Congratulation! ✓", align="center", 
                      font=("Arial", 14, "bold"))
        
    def start_game(self):
        """开始游戏 - 根据条件选择进入的游戏模式"""
        # 检查是否达成所有条件
        all_conditions_met = (self.manager.save_data.purple_completed and 
                             self.manager.save_data.blue_completed and 
                             self.manager.save_data.red_mode_completed)
        
        if all_conditions_met:
            # 进入普通贪吃蛇模式
            self.manager.reset_game_score()
            self.manager.change_state(GameState.NORMAL_SNAKE)
        else:
            # 进入原始的三色选择模式
            self.manager.reset_game_score()
            self.manager.change_state(GameState.SNAKE_GAME)
        
    def run(self):
        self.clear_screen()
        self.create_title_art()
        self.manager.score_display.update()
        
        # 绑定按键
        self.screen.listen()
        self.screen.onkeypress(self.start_game, "space")
        
        # 修复：添加状态检查，确保状态改变时立即退出循环
        while self.manager.current_state == GameState.TITLE:
            self.screen.update()
            time.sleep(0.1)
            # 关键修复：状态改变时立即退出循环
            if self.manager.current_state != GameState.TITLE:
                break