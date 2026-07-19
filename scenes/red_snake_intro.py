import turtle
import time
import math
from scenes.base_scene import BaseScene
from constants import GameState

class RedSnakeIntro(BaseScene):
    def __init__(self, game_manager):
        super().__init__(game_manager)
        self.transition_complete = False
        
    def create_red_transition(self):
        """创建红色过渡特效"""
        # 创建多个红色方块形成螺旋
        segments = []
        num_segments = 20
        center_x, center_y = 0, 0
        spiral_radius = 10
        
        for i in range(num_segments):
            segment = turtle.Turtle()
            segment.shape("square")
            segment.color("red")
            segment.penup()
            segment.goto(center_x, center_y)
            segments.append(segment)
        
        # 螺旋展开动画
        for step in range(30):
            for i, segment in enumerate(segments):
                angle = i * 0.3 + step * 0.1
                radius = spiral_radius + step * 8
                
                spiral_x = center_x + radius * math.cos(angle)
                spiral_y = center_y + radius * math.sin(angle)
                
                segment.goto(spiral_x, spiral_y)
                red_intensity = max(0.3, 1.0 - i / len(segments))
                segment.color(f"#{int(200 * red_intensity):02x}0000")
            
            self.screen.update()
            time.sleep(0.05)
        
        # 红色方块充满屏幕
        red_square = turtle.Turtle()
        red_square.hideturtle()
        red_square.penup()
        red_square.color("red")
        red_square.goto(0, 0)
        
        for size in range(0, 500, 15):
            red_square.clear()
            red_square.dot(size)
            self.screen.update()
            time.sleep(0.02)
        
        # 红色方块缩小，显示游戏标题
        for size in range(500, 0, -15):
            red_square.clear()
            if size > 0:
                red_square.dot(size)
            self.screen.update()
            time.sleep(0.02)
        
        # 清除所有元素
        red_square.hideturtle()
        for segment in segments:
            segment.hideturtle()
            
        self.transition_complete = True
        
    def show_cerberus_title(self):
        """显示Cerberus标题"""
        self.clear_screen()
        
        # Cerberus 实心艺术字
        title_turtle = turtle.Turtle()
        title_turtle.hideturtle()
        title_turtle.penup()
        title_turtle.color("#FF0000")
        
        cerberus_art = [
            " ██████ ███████ ██████  ██████ ███████ ██████  ██    ██ ██ ███████ ",
            "██      ██      ██   ██ ██   ██ ██      ██   ██ ██    ██ ██ ██      ",
            "██      █████   ██████  ██████  █████   ██████  ██    ██ ██ ███████ ",
            "██      ██      ██   ██ ██   ██ ██      ██   ██  ██  ██  ██      ██ ",
            " ██████ ███████ ██   ██ ██   ██ ███████ ██   ██   ████   ██ ███████ "
        ]
        
        for i, line in enumerate(cerberus_art):
            title_turtle.goto(-350, 150 - i * 30)
            title_turtle.write(line, align="left", font=("Courier", 10, "bold"))
        
        # 副标题
        subtitle = turtle.Turtle()
        subtitle.hideturtle()
        subtitle.penup()
        subtitle.color("#FF0000")
        subtitle.goto(0, -50)
        subtitle.write("Rascal Snake", align="center", font=("Arial", 20, "bold"))
        
        # 游戏说明
        instructions = turtle.Turtle()
        instructions.hideturtle()
        instructions.penup()
        instructions.color("#FF4444")
        instructions.goto(0, -100)
        instructions.write("HELP! Reach 333 points to RELEASE ME!", 
                          align="center", font=("Arial", 14, "normal"))
        
        # 开始提示
        prompt = turtle.Turtle()
        prompt.hideturtle()
        prompt.penup()
        prompt.color("#00FF00")
        prompt.goto(0, -180)
        prompt.write("Press SPACE to start the game", 
                   align="center", font=("Arial", 16, "bold"))
        
        self.screen.update()
        
    def start_game(self):
        """开始游戏"""
        self.manager.change_state(GameState.RED_SNAKE)
        
    def run(self):
        """运行过渡场景"""
        self.clear_screen()
        
        # 红色过渡特效
        self.create_red_transition()
        
        # 显示游戏标题和说明
        self.show_cerberus_title()
        
        # 绑定按键
        self.screen.listen()
        self.screen.onkeypress(self.start_game, "space")
        
        # 等待玩家按空格开始游戏
        while self.manager.current_state == GameState.RED_SNAKE_INTRO:
            self.screen.update()
            time.sleep(0.1)