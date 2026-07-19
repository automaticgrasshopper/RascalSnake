import turtle
import time
import math
from scenes.base_scene import BaseScene
from constants import GameState

class BlueModeIntro(BaseScene):
    def __init__(self, game_manager):
        super().__init__(game_manager)
        
    def run(self):
        self.clear_screen()
        
        # 第一步：蓝色蛇蜷缩成回字形立方体
        self.create_blue_spiral()
        
        # 第二步：蓝色方块充满屏幕
        blue_square = turtle.Turtle()
        blue_square.hideturtle()
        blue_square.penup()
        blue_square.color("blue")
        blue_square.goto(0, 0)
        
        # 蓝色方块从中心扩展到充满屏幕
        for size in range(0, 500, 10):
            blue_square.clear()
            blue_square.dot(size)
            self.screen.update()
            time.sleep(0.02)
        
        # 第三步：蓝色方块缩小成呼吸立方体
        cube_size = 100
        cube = turtle.Turtle()
        cube.hideturtle()
        cube.penup()
        cube.color("blue")
        cube.goto(0, 200)
        
        # 呼吸动画
        for breath in range(10):
            current_size = cube_size + math.sin(breath * 0.5) * 20
            cube.clear()
            cube.dot(current_size)
            self.screen.update()
            time.sleep(0.2)
        
        # 第四步：显示MATRIX艺术字和开始提示
        self.show_matrix_title()
        
        # 第五步：浮上挡板和小球
        self.create_paddle_and_ball()
        
        # 设置空格键开始游戏
        self.screen.listen()
        self.screen.onkeypress(self.start_breakout, "space")
        
        # 等待玩家按空格
        while self.manager.current_state == GameState.BLUE_MODE:
            self.screen.update()
            time.sleep(0.1)
            if self.manager.current_state != GameState.BLUE_MODE:
                break
    
    def create_blue_spiral(self):
        """创建蓝色蛇蜷缩成回字形的动画"""
        # 创建多个蓝色方块模拟蛇身
        segments = []
        num_segments = 20
        center_x, center_y = 0, 0
        spiral_radius = 150  # 初始螺旋半径
        
        # 创建蛇身段
        for i in range(num_segments):
            segment = turtle.Turtle()
            segment.shape("square")
            segment.color("blue")
            segment.penup()
            segment.goto(center_x, center_y)
            segments.append(segment)
        
        # 蜷缩动画 - 蛇身逐渐形成螺旋形
        for step in range(30):
            for i, segment in enumerate(segments):
                # 计算螺旋角度
                angle = i * 0.3 + step * 0.1
                # 计算螺旋半径（逐渐缩小）
                radius = spiral_radius * (1 - step / 40)
                
                # 计算螺旋坐标
                spiral_x = center_x + radius * math.cos(angle)
                spiral_y = center_y + radius * math.sin(angle)
                
                # 移动蛇段到螺旋位置
                segment.goto(spiral_x, spiral_y)
                
                # 蛇段逐渐变成深蓝色
                blue_intensity = max(0.3, 1.0 - i / len(segments))
                segment.color(f"#{int(100 * blue_intensity):02x}{int(100 * blue_intensity):02x}FF")
            
            self.screen.update()
            time.sleep(0.05)
        
        # 形成立方体
        cube_size = 40
        for step in range(20):
            for i, segment in enumerate(segments):
                # 计算立方体位置
                if i == 0:  # 中心
                    target_x, target_y = center_x, center_y
                elif i % 4 == 1:  # 上
                    target_x, target_y = center_x, center_y + cube_size
                elif i % 4 == 2:  # 右
                    target_x, target_y = center_x + cube_size, center_y
                elif i % 4 == 3:  # 下
                    target_x, target_y = center_x, center_y - cube_size
                else:  # 左
                    target_x, target_y = center_x - cube_size, center_y
                
                # 平滑移动到目标位置
                current_x, current_y = segment.position()
                segment.goto(
                    current_x + (target_x - current_x) * 0.2,
                    current_y + (target_y - current_y) * 0.2
                )
                
                # 所有蛇段变成深蓝色
                segment.color("#0000FF")
                
            self.screen.update()
            time.sleep(0.05)
        
        # 清除蛇身段
        for segment in segments:
            segment.hideturtle()
            
    def create_paddle_and_ball(self):
        self.paddle = turtle.Turtle()
        self.paddle.shape("square")
        self.paddle.color("white")
        self.paddle.shapesize(1, 5)
        self.paddle.penup()
        self.paddle.goto(0, -250)
        
        self.ball = turtle.Turtle()
        self.ball.shape("circle")
        self.ball.color("white")
        self.ball.penup()
        self.ball.goto(0, -230)
        
        self.screen.update()
        
    def show_matrix_title(self):
        """显示MATRIX艺术字"""
        # MATRIX ASCII艺术字
        matrix_art = [
            "███╗   ███╗ █████╗ ████████╗██████╗ ██╗██╗  ██╗",
            "████╗ ████║██╔══██╗╚══██╔══╝██╔══██╗██║╚██╗██╔╝", 
            "██╔████╔██║███████║   ██║   ██████╔╝██║ ╚███╔╝ ",
            "██║╚██╔╝██║██╔══██║   ██║   ██╔══██╗██║ ██╔██╗ ",
            "██║ ╚═╝ ██║██║  ██║   ██║   ██║  ██║██║██╔╝ ██╗",
            "╚═╝     ╚═╝╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝╚═╝╚═╝  ╚═╝"
        ]
        
        # 显示MATRIX艺术字
        matrix_turtle = turtle.Turtle()
        matrix_turtle.hideturtle()
        matrix_turtle.penup()
        matrix_turtle.color("white")
        
        for i, line in enumerate(matrix_art):
            matrix_turtle.goto(-350, 100 - i * 20)
            matrix_turtle.write(line, align="left", font=("Courier", 10, "normal"))
        
        # 副标题
        subtitle = turtle.Turtle()
        subtitle.hideturtle()
        subtitle.penup()
        subtitle.color("white")
        subtitle.goto(0, -50)
        subtitle.write("BLUE MODE", align="center", font=("Arial", 18, "bold"))
        
        # 开始提示
        prompt = turtle.Turtle()
        prompt.hideturtle()
        prompt.penup()
        prompt.color("white")
        prompt.goto(0, -100)
        prompt.write("Press SPACE to start", align="center", font=("Arial", 16, "normal"))
        
    def start_breakout(self):
        self.manager.change_state(GameState.BLUE_BREAKOUT)