import turtle
import time
import math
from scenes.base_scene import BaseScene
from constants import GameState, BLUE_BLOCK_POINTS

class BlueBreakout(BaseScene):
    def __init__(self, game_manager):
        super().__init__(game_manager)
        self.ball_dx = 5
        self.ball_dy = -5
        self.paddle_width = 5
        self.blocks = []
        self.breathing_cube = None
        self.game_started = False
        self.paddle_speed = 30
        
    def create_breathing_cube(self):
        self.breathing_cube = turtle.Turtle()
        self.breathing_cube.hideturtle()
        self.breathing_cube.penup()
        self.breathing_cube.color("blue")
        self.breathing_cube.goto(0, 280)
        
    def create_blocks(self):
        block_colors = [
            "#0000FF",
            "#3333FF",
            "#6666FF",
            "#9999FF"
        ]
        
        block_width = 60
        block_height = 30
        start_x = -300
        start_y = 100
        
        self.blocks = []
        
        for row in range(4):
            color = block_colors[row]
            for col in range(10):
                block = turtle.Turtle()
                block.shape("square")
                block.color(color)
                block.shapesize(block_height/20, block_width/20)
                block.penup()
                
                x = start_x + col * (block_width + 10)
                y = start_y - row * (block_height + 10)
                block.goto(x, y)
                
                self.blocks.append(block)
                
    def create_paddle(self):
        self.paddle = turtle.Turtle()
        self.paddle.shape("square")
        self.paddle.color("white")
        self.paddle.shapesize(1, self.paddle_width)
        self.paddle.penup()
        self.paddle.goto(0, -250)
        
    def create_ball(self):
        self.ball = turtle.Turtle()
        self.ball.shape("circle")
        self.ball.color("white")
        self.ball.penup()
        self.ball.goto(0, -230)
        
    def move_paddle_left(self):
        x = self.paddle.xcor()
        new_x = x - self.paddle_speed
        if new_x > -350:
            self.paddle.setx(new_x)
        else:
            self.paddle.setx(-350)
            
    def move_paddle_right(self):
        x = self.paddle.xcor()
        new_x = x + self.paddle_speed
        if new_x < 350:
            self.paddle.setx(new_x)
        else:
            self.paddle.setx(350)
            
    def update_breathing_cube(self):
        if self.breathing_cube:
            size = 80 + math.sin(time.time() * 2) * 10
            self.breathing_cube.clear()
            self.breathing_cube.dot(size)
            
    def check_ball_collision(self):
        ball_x, ball_y = self.ball.position()
        
        # 检查墙壁碰撞
        if ball_x > 390 or ball_x < -390:
            self.ball_dx *= -1
            
        if ball_y > 290:
            self.ball_dy *= -1
            
        # 检查底部边界（游戏结束）
        if ball_y < -290:
            self.game_over()
            return True
            
        # 检查挡板碰撞
        paddle_left = self.paddle.xcor() - self.paddle_width * 10
        paddle_right = self.paddle.xcor() + self.paddle_width * 10
        
        if (ball_y < -240 and ball_y > -250 and 
            paddle_left < ball_x < paddle_right):
            # 根据击中挡板的位置调整反弹角度
            paddle_center = self.paddle.xcor()
            offset = (ball_x - paddle_center) / (self.paddle_width * 10)
            self.ball_dx = offset * 6
            self.ball_dy *= -1
            
        # 检查砖块碰撞
        for block in self.blocks[:]:
            block_x, block_y = block.position()
            block_width = 60
            block_height = 30
            
            if (abs(ball_x - block_x) < block_width/2 + 10 and 
                abs(ball_y - block_y) < block_height/2 + 10):
                
                block.hideturtle()
                self.blocks.remove(block)
                
                self.manager.add_score(BLUE_BLOCK_POINTS)
                
                # 移除挡板缩短逻辑
                
                # 根据碰撞位置决定反弹方向
                if abs(ball_x - block_x) > abs(ball_y - block_y):
                    self.ball_dx *= -1
                else:
                    self.ball_dy *= -1
                    
                break
                
        # 检查呼吸立方体碰撞（游戏胜利）
        if ball_y > 250 and abs(ball_x) < 50:
            self.victory()
            return True
            
        return False
        
    def move_ball(self):
        self.ball.setx(self.ball.xcor() + self.ball_dx)
        self.ball.sety(self.ball.ycor() + self.ball_dy)
        
    def game_over(self):
        # 显示游戏结束文字
        game_over_text = turtle.Turtle()
        game_over_text.hideturtle()
        game_over_text.penup()
        game_over_text.color("white")
        game_over_text.goto(0, -100)
        game_over_text.write("GAME OVER", align="center", font=("Arial", 24, "bold"))
        
        restart_text = turtle.Turtle()
        restart_text.hideturtle()
        restart_text.penup()
        restart_text.color("yellow")
        restart_text.goto(0, -150)
        restart_text.write("Press R to Restart", align="center", font=("Arial", 16, "normal"))
        
        self.screen.update()
        
        self.screen.listen()
        self.screen.onkeypress(self.restart_to_title, "r")  # 改回：回到标题
        self.screen.onkeypress(self.restart_to_title, "R")
        
        while True:
            self.screen.update()
            time.sleep(0.1)
            if self.manager.current_state != GameState.BLUE_BREAKOUT:
                break
            
    def victory(self):
        # 显示胜利文字
        victory_text = turtle.Turtle()
        victory_text.hideturtle()
        victory_text.penup()
        victory_text.color("white")
        victory_text.goto(0, -100)
        victory_text.write("VICTORY!", align="center", font=("Arial", 24, "bold"))
        
        score_text = turtle.Turtle()
        score_text.hideturtle()
        score_text.penup()
        score_text.color("white")
        score_text.goto(0, -150)
        score_text.write(f"Score: {self.manager.current_game_score}", align="center", font=("Arial", 16, "normal"))
        
        # 修改：不再提示按R继续，而是自动进入飞机游戏
        continue_text = turtle.Turtle()
        continue_text.hideturtle()
        continue_text.penup()
        continue_text.color("yellow")
        continue_text.goto(0, -200)
        continue_text.write("Loading...", align="center", font=("Arial", 16, "normal"))
        
        self.screen.update()
        # 等待1秒后自动进入飞机游戏
        time.sleep(1)
        self.manager.change_state(GameState.BLUE_PLANE)  # 切换到飞机游戏
            
    def restart_to_title(self):
        """重新开始游戏，回到标题界面"""  # 改回：回到标题
        self.manager.reset_game_score()
        self.manager.change_state(GameState.TITLE)
        
    def run(self):
        """运行打砖块游戏"""
        self.clear_screen()
        self.manager.score_display.update()
        
        # 创建游戏元素
        self.create_breathing_cube()
        self.create_blocks()
        self.create_paddle()
        self.create_ball()
        
        # 绑定按键
        self.screen.listen()
        self.screen.onkeypress(self.move_paddle_left, "Left")
        self.screen.onkeypress(self.move_paddle_right, "Right")
        self.screen.onkeypress(self.restart_to_title, "r")  # 改回：回到标题
        self.screen.onkeypress(self.restart_to_title, "R")
        
        self.game_started = True
        
        # 游戏主循环
        while self.manager.current_state == GameState.BLUE_BREAKOUT and self.game_started:
            self.move_ball()
            
            if self.check_ball_collision():
                break
                
            self.update_breathing_cube()
            self.screen.update()
            time.sleep(0.016)  # 约60帧，提高流畅度
            
            if self.manager.current_state != GameState.BLUE_BREAKOUT:
                break