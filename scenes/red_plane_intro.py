import turtle
import time
import math
from scenes.base_scene import BaseScene
from constants import GameState

class RedPlaneIntro(BaseScene):
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
        
        # 红色方块缩小，显示游戏标题和第一帧
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
        
    def create_plane_first_frame(self):
        """创建飞机游戏的第一帧画面"""
        elements = []
        
        # 创建玩家飞机（白色三角）在底部中央
        player = turtle.Turtle()
        player.hideturtle()
        player.penup()
        player.shape("triangle")
        player.color("white")
        player.shapesize(1.5, 1.5)
        player.goto(0, -180)
        player.setheading(90)
        player.showturtle()
        elements.append(player)
        
        # 创建蓝色敌机阵型 - 在玩家上方形成弧形
        blue_enemies = []
        blue_positions = [(-150, 80), (-50, 120), (50, 120), (150, 80)]
        for pos in blue_positions:
            enemy = turtle.Turtle()
            enemy.hideturtle()
            enemy.penup()
            enemy.shape("triangle")
            enemy.color("blue")
            enemy.shapesize(1.2, 1.2)
            enemy.goto(pos[0], pos[1])
            enemy.setheading(270)
            enemy.showturtle()
            blue_enemies.append(enemy)
            elements.append(enemy)
        
        # 创建紫色敌机阵型 - 在更上方
        purple_enemies = []
        purple_positions = [(-100, 180), (0, 200), (100, 180)]
        for pos in purple_positions:
            enemy = turtle.Turtle()
            enemy.hideturtle()
            enemy.penup()
            enemy.shape("triangle")
            enemy.color("#8A2BE2")
            enemy.shapesize(1.2, 1.2)
            enemy.goto(pos[0], pos[1])
            enemy.setheading(270)
            enemy.showturtle()
            purple_enemies.append(enemy)
            elements.append(enemy)
        
        # 创建玩家子弹轨迹效果
        bullets = []
        for i in range(3):
            bullet = turtle.Turtle()
            bullet.hideturtle()
            bullet.penup()
            bullet.shape("circle")
            bullet.color("cyan")
            bullet.shapesize(0.4, 0.4)
            bullet.goto(-10 + i * 10, -120 + i * 40)
            bullet.showturtle()
            bullets.append(bullet)
            elements.append(bullet)
        
        # 创建敌机子弹轨迹效果
        enemy_bullets = []
        enemy_bullet_positions = [(-150, 40), (0, 60), (150, 40)]
        for pos in enemy_bullet_positions:
            bullet = turtle.Turtle()
            bullet.hideturtle()
            bullet.penup()
            bullet.shape("circle")
            bullet.color("red")
            bullet.shapesize(0.3, 0.3)
            bullet.goto(pos[0], pos[1])
            bullet.showturtle()
            enemy_bullets.append(bullet)
            elements.append(bullet)
        
        return elements
        
    def show_party_title(self):
        """显示PARTY标题与飞机游戏第一帧"""
        self.clear_screen()
        
        # 先创建飞机游戏的第一帧作为背景
        self.game_frame_elements = self.create_plane_first_frame()
        
        # 在半透明黑色覆盖层上显示标题，确保文字可读
        overlay = turtle.Turtle()
        overlay.hideturtle()
        overlay.penup()
        overlay.color("black")
        overlay.goto(0, 0)
        overlay.dot(800)  # 大黑圆作为背景
        self.game_frame_elements.append(overlay)
        
        title_turtle = turtle.Turtle()
        title_turtle.hideturtle()
        title_turtle.penup()
        title_turtle.color("red")
        
        # PARTY 艺术字
        title_art = [
            "██████╗  █████╗ ██████╗ ████████╗██╗   ██╗",
            "██╔══██╗██╔══██╗██╔══██╗╚══██╔══╝╚██╗ ██╔╝", 
            "██████╔╝███████║██████╔╝   ██║    ╚████╔╝ ",
            "██╔═══╝ ██╔══██║██╔══██╗   ██║     ╚██╔╝  ",
            "██║     ██║  ██║██║  ██║   ██║      ██║   ",
            "╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝      ╚═╝   "
        ]
        
        for i, line in enumerate(title_art):
            title_turtle.goto(-250, 80 - i * 25)
            title_turtle.write(line, align="left", font=("Courier", 10, "bold"))
        
        # 副标题
        subtitle = turtle.Turtle()
        subtitle.hideturtle()
        subtitle.penup()
        subtitle.color("white")
        subtitle.goto(0, -80)
        subtitle.write("PARTY", align="center", font=("Arial", 24, "bold"))
        
        # 开始提示
        prompt = turtle.Turtle()
        prompt.hideturtle()
        prompt.penup()
        prompt.color("yellow")
        prompt.goto(0, -220)
        prompt.write("Press SPACE to start", align="center", font=("Arial", 16, "normal"))
        
        self.screen.update()
        
    def start_game(self):
        """开始游戏"""
        # 隐藏所有第一帧元素
        for element in self.game_frame_elements:
            element.hideturtle()
        self.manager.change_state(GameState.RED_PLANE)
        
    def run(self):
        """运行红色飞机介绍场景"""
        self.clear_screen()
        
        # 红色过渡特效
        self.create_red_transition()
        
        # 显示游戏标题和第一帧画面
        self.show_party_title()
        
        # 绑定按键
        self.screen.listen()
        self.screen.onkeypress(self.start_game, "space")
        
        # 等待玩家按空格开始游戏
        while self.manager.current_state == GameState.RED_PLANE_INTRO:
            self.screen.update()
            time.sleep(0.1)