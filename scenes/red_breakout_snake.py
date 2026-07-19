import turtle
import time
import random
import math
from scenes.base_scene import BaseScene
from constants import GameState, RED_SNAKE_FOOD_POINTS

class RedBreakoutSnake(BaseScene):
    def __init__(self, game_manager):
        super().__init__(game_manager)
        self.snake = []  # 红色渐变蛇
        self.food = None
        self.blocks = []  # 红色砖块
        self.direction = "Right"
        self.next_direction = "Right"
        self.is_dead = False
        self.game_started = True
        self.snake_speed = 3  # 蛇模式移动速度（帧数控制）
        self.move_counter = 0
        self.food_move_counter = 0
        
    def create_initial_blocks(self):
        """创建初始砖块（从red_breakout.py复制）"""
        block_colors = [
            "#FF0000",
            "#FF3333",
            "#FF6666",
            "#FF9999"
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
                
    def create_food(self):
        """创建红色食物（从呼吸立方体变化而来）"""
        self.food = turtle.Turtle()
        self.food.shape("circle")
        self.food.color("#FF0000")
        self.food.penup()
        # 位置在顶部中央
        self.food.goto(0, 280)
        # 变小成食物大小
        self.food.shapesize(0.5, 0.5)  # 比普通蛇食物稍大
        
    def create_snake(self, paddle_segments):
        """从打砖块的挡板创建蛇，保持相同位置和颜色"""
        self.snake = []
        
        # 复制挡板段作为蛇的初始段
        for i, segment in enumerate(paddle_segments):
            snake_segment = turtle.Turtle()
            snake_segment.shape("square")
            
            # 保持相同的红色渐变
            red_intensity = max(100, 255 - i * 40)
            snake_segment.color(f"#{red_intensity:02x}0000")
            
            snake_segment.penup()
            # 保持相同位置
            snake_segment.goto(segment.xcor(), segment.ycor())
            self.snake.append(snake_segment)
            
    def move_snake(self):
        """移动蛇"""
        self.move_counter += 1
        if self.move_counter < self.snake_speed:  # 控制蛇的移动速度
            return
        self.move_counter = 0
        
        self.direction = self.next_direction
        
        # 移动身体段
        for i in range(len(self.snake) - 1, 0, -1):
            x = self.snake[i-1].xcor()
            y = self.snake[i-1].ycor()
            self.snake[i].goto(x, y)
            
        # 移动头部
        head = self.snake[0]
        if self.direction == "Up":
            head.sety(head.ycor() + 20)
        elif self.direction == "Down":
            head.sety(head.ycor() - 20)
        elif self.direction == "Left":
            head.setx(head.xcor() - 20)
        elif self.direction == "Right":
            head.setx(head.xcor() + 20)
            
    def check_collision(self):
        """检查碰撞"""
        head = self.snake[0]
        
        # 检查边界碰撞 - 碰到边缘随机转向
        if head.xcor() > 380 or head.xcor() < -380 or head.ycor() > 280 or head.ycor() < -280:
            self.random_turn()
            return False
                
        # 检查自身碰撞
        for segment in self.snake[1:]:
            if head.distance(segment) < 10:
                return True
                
        return False
        
    def random_turn(self):
        """随机转向，避免原方向的反方向"""
        head = self.snake[0]
        
        # 根据当前位置决定可能的转向
        possible_directions = []
        
        if head.xcor() > 380:  # 碰到右边界
            possible_directions = ["Up", "Down", "Left"]
        elif head.xcor() < -380:  # 碰到左边界
            possible_directions = ["Up", "Down", "Right"]
        elif head.ycor() > 280:  # 碰到上边界
            possible_directions = ["Left", "Right", "Down"]
        elif head.ycor() < -280:  # 碰到下边界
            possible_directions = ["Left", "Right", "Up"]
            
        # 移除当前方向的反方向（避免立即回头）
        opposite_directions = {
            "Up": "Down",
            "Down": "Up", 
            "Left": "Right",
            "Right": "Left"
        }
        
        if self.direction in possible_directions:
            possible_directions.remove(self.direction)
            
        opposite = opposite_directions.get(self.direction)
        if opposite in possible_directions:
            possible_directions.remove(opposite)
            
        # 随机选择一个方向
        if possible_directions:
            self.next_direction = random.choice(possible_directions)
        
    def check_block_collision(self):
        """检查砖块碰撞 - 撞破红色砖块，得到50分"""
        head = self.snake[0]
        blocks_to_remove = []
        
        for block in self.blocks:
            if head.distance(block) < 30:  # 碰撞检测
                blocks_to_remove.append(block)
                
        # 移除碰撞到的砖块
        for block in blocks_to_remove:
            block.hideturtle()
            self.blocks.remove(block)
            # 撞破砖块得到50分
            self.manager.add_score(50)
            
        return len(blocks_to_remove) > 0
        
    def check_food_collision(self):
        """检查食物碰撞"""
        head = self.snake[0]
        
        if head.distance(self.food) < 25:  # 吃到食物
            self.manager.add_score(RED_SNAKE_FOOD_POINTS)  # 吃到食物加666分
            return True
                
        return False
        
    def add_segment(self):
        """添加蛇身段"""
        segment = turtle.Turtle()
        segment.shape("square")
        # 根据蛇长度选择红色强度
        color_index = min(len(self.snake) - 1, 5)
        red_intensity = 255 - color_index * 40
        segment.color(f"#{max(100, red_intensity):02x}0000")
        segment.penup()
        last_segment = self.snake[-1]
        segment.goto(last_segment.xcor(), last_segment.ycor())
        self.snake.append(segment)
        
    def go_up(self):
        if self.direction != "Down":
            self.next_direction = "Up"
            
    def go_down(self):
        if self.direction != "Up":
            self.next_direction = "Down"
            
    def go_left(self):
        if self.direction != "Right":
            self.next_direction = "Left"
            
    def go_right(self):
        if self.direction != "Left":
            self.next_direction = "Right"
            
    def game_over(self):
        """游戏结束"""
        self.is_dead = True
        
        # 显示死亡提示
        death_text = turtle.Turtle()
        death_text.hideturtle()
        death_text.penup()
        death_text.color("white")
        death_text.goto(0, 0)
        death_text.write("GAME OVER", align="center", font=("Arial", 24, "bold"))
        
        restart_text = turtle.Turtle()
        restart_text.hideturtle()
        restart_text.penup()
        restart_text.color("yellow")
        restart_text.goto(0, -50)
        restart_text.write("Press R to return to Title", align="center", font=("Arial", 16, "normal"))
        
        self.screen.update()
        
        # 设置R键监听器
        self.screen.listen()
        self.screen.onkeypress(self.return_to_title, "r")
        self.screen.onkeypress(self.return_to_title, "R")
        
    def snake_victory(self):
        """蛇模式胜利"""
        victory_text = turtle.Turtle()
        victory_text.hideturtle()
        victory_text.penup()
        victory_text.color("red")
        victory_text.goto(0, -100)
        victory_text.write("SNAKE VICTORY!", align="center", font=("Arial", 24, "bold"))
        
        score_text = turtle.Turtle()
        score_text.hideturtle()
        score_text.penup()
        score_text.color("white")
        score_text.goto(0, -150)
        score_text.write(f"Score: {self.manager.current_game_score}", align="center", font=("Arial", 16, "normal"))
        
        continue_text = turtle.Turtle()
        continue_text.hideturtle()
        continue_text.penup()
        continue_text.color("yellow")
        continue_text.goto(0, -200)
        continue_text.write("Loading...", align="center", font=("Arial", 16, "normal"))
        
        self.screen.update()
        # 等待1秒后自动进入下一个游戏
        time.sleep(0)
        self.manager.change_state(GameState.RED_PLANE_INTRO)
            
    def return_to_title(self):
        """返回标题"""
        self.manager.reset_game_score()
        self.manager.change_state(GameState.TITLE)
        
    def run(self, previous_scene=None):
        """运行红色打砖块蛇模式
        previous_scene: 之前的打砖块场景，用于获取当前状态
        """
        self.clear_screen()
        self.manager.score_display.update()
        
        # 从之前的场景获取当前状态
        if previous_scene:
            # 创建相同的砖块布局
            self.create_initial_blocks()
            # 从挡板创建蛇，保持相同位置
            self.create_snake(previous_scene.paddle_segments)
        else:
            # 如果没有提供之前的场景，创建默认状态
            self.create_initial_blocks()
            self.create_snake([])
            
        # 创建食物（变小的红色立方体）
        self.create_food()
        
        # 绑定按键
        self.screen.listen()
        self.screen.onkeypress(self.go_up, "Up")
        self.screen.onkeypress(self.go_down, "Down")
        self.screen.onkeypress(self.go_left, "Left")
        self.screen.onkeypress(self.go_right, "Right")
        self.screen.onkeypress(self.return_to_title, "r")
        self.screen.onkeypress(self.return_to_title, "R")
        
        # 游戏主循环
        while self.manager.current_state == GameState.RED_BREAKOUT_SNAKE and not self.is_dead:
            self.move_snake()
            
            # 检查各种碰撞
            if self.check_collision():
                self.game_over()
                break
                
            self.check_block_collision()  # 撞破砖块，会得到50分
            
            if self.check_food_collision():
                # 吃到食物就胜利
                self.snake_victory()
                break
                        
            self.screen.update()
            time.sleep(0.016)  # 约60帧
            
        # 游戏结束处理
        if self.is_dead:
            while self.manager.current_state == GameState.RED_BREAKOUT_SNAKE:
                self.screen.update()
                time.sleep(0.1)