import turtle
import time
import random
import math
from scenes.base_scene import BaseScene
from constants import GameState

class RedSnakeGame(BaseScene):
    def __init__(self, game_manager):
        super().__init__(game_manager)
        self.reset_game_state()
        
    def reset_game_state(self):
        """完全重置游戏状态"""
        self.snake = []  # 玩家蛇
        self.enemy_snakes = []  # 敌对蛇
        self.enemy_directions = []  # 敌方蛇的方向
        self.food = None
        self.bullets = []  # 子弹
        self.direction = "Right"
        self.next_direction = "Right"
        self.is_dead = False
        self.game_started = True  # 直接开始游戏
        self.enemy_move_counter = 0
        self.particles = []
        self.death_animation_complete = False
        
    def create_walls(self):
        """创建围墙"""
        self.walls = []
        
        # 上下围墙
        for x in range(-380, 381, 20):
            wall_top = self.create_wall_segment(x, 280)
            wall_bottom = self.create_wall_segment(x, -300)
            self.walls.extend([wall_top, wall_bottom])
            
        # 左右围墙
        for y in range(-280, 301, 20):
            wall_left = self.create_wall_segment(-400, y)
            wall_right = self.create_wall_segment(380, y)
            self.walls.extend([wall_left, wall_right])
            
    def create_wall_segment(self, x, y):
        """创建单个围墙段"""
        wall = turtle.Turtle()
        wall.shape("square")
        wall.color("#808080")
        wall.penup()
        wall.goto(x, y)
        return wall
        
    def create_player_snake(self):
        """创建红色渐变玩家蛇，从中心开始"""
        start_x, start_y = 0, 0
        
        for i in range(3):
            segment = turtle.Turtle()
            
            # 红色渐变
            if i == 0:  # 蛇头 - 三角形
                segment.shape("triangle")
                segment.color("#FF0000")
            else:  # 蛇身使用红色渐变
                red_intensity = max(100, 255 - i * 40)
                segment.color(f"#{red_intensity:02x}0000")
                segment.shape("square")
                
            segment.penup()
            segment_x = start_x - i * 20
            segment_y = start_y
            segment.goto(segment_x, segment_y)
            self.snake.append(segment)
            
    def create_enemy_snakes(self):
        """创建敌对蛇（蓝色和紫色）- 舒展的8节蛇身"""
        self.enemy_snakes = []
        self.enemy_directions = []  # 重置方向列表
        
        # 蓝色敌对蛇 - 左上角，水平舒展
        blue_snake = []
        blue_start_x, blue_start_y = -300, 200
        
        for i in range(8):  # 8节长度
            segment = turtle.Turtle()
            segment.shape("square")
            # 蓝色渐变
            blue_intensity = max(100, 255 - i * 20)  # 更平缓的渐变
            segment.color(f"#0000{blue_intensity:02x}")
            segment.penup()
            segment_x = blue_start_x + i * 20  # 水平排列
            segment_y = blue_start_y
            segment.goto(segment_x, blue_start_y)
            blue_snake.append(segment)
        
        # 紫色敌对蛇 - 右上角，水平舒展
        purple_snake = []
        purple_start_x, purple_start_y = 200, 200
        
        for i in range(8):  # 8节长度
            segment = turtle.Turtle()
            segment.shape("square")
            # 紫色渐变
            purple_intensity = max(100, 255 - i * 20)  # 更平缓的渐变
            segment.color(f"#{purple_intensity:02x}00{purple_intensity:02x}")
            segment.penup()
            segment_x = purple_start_x - i * 20  # 水平排列，向左延伸
            segment_y = purple_start_y
            segment.goto(segment_x, purple_start_y)
            purple_snake.append(segment)
            
        self.enemy_snakes = [blue_snake, purple_snake]
        # 初始化敌方蛇的方向
        self.enemy_directions = ["Right", "Left"]
        
    def create_food(self):
        """创建红色食物"""
        self.food = turtle.Turtle()
        self.food.shape("circle")
        self.food.color("#FF0000")
        self.food.penup()
        self.move_food()
        
    def move_food(self):
        """移动食物到随机位置"""
        while True:
            x = (random.randint(-17, 17) * 20)
            y = (random.randint(-12, 12) * 20)
            if (-360 <= x <= 360 and -260 <= y <= 260):
                self.food.goto(x, y)
                break
                
    def move_enemy_snakes(self):
        """移动敌对蛇 - 随机自由移动，避免自身重叠"""
        if not self.game_started or self.is_dead:
            return
            
        self.enemy_move_counter += 1
        # 每3帧移动一次敌对蛇
        if self.enemy_move_counter < 3:
            return
            
        self.enemy_move_counter = 0
        
        for idx, enemy_snake in enumerate(self.enemy_snakes):
            if not enemy_snake:
                continue
                
            head = enemy_snake[0]
            
            # 随机决定是否改变方向（约30%的概率）
            if random.random() < 0.3:
                # 获取当前可能的移动方向
                possible_directions = []
                current_x, current_y = head.position()
                
                # 检查各个方向是否安全（不会撞墙且不会与自身重叠）
                # 上
                new_x, new_y = current_x, current_y + 20
                if (-360 <= new_x <= 360 and -260 <= new_y <= 260 and 
                    not self.will_collide_with_self(enemy_snake, new_x, new_y)):
                    possible_directions.append("Up")
                
                # 下
                new_x, new_y = current_x, current_y - 20
                if (-360 <= new_x <= 360 and -260 <= new_y <= 260 and 
                    not self.will_collide_with_self(enemy_snake, new_x, new_y)):
                    possible_directions.append("Down")
                
                # 左
                new_x, new_y = current_x - 20, current_y
                if (-360 <= new_x <= 360 and -260 <= new_y <= 260 and 
                    not self.will_collide_with_self(enemy_snake, new_x, new_y)):
                    possible_directions.append("Left")
                
                # 右
                new_x, new_y = current_x + 20, current_y
                if (-360 <= new_x <= 360 and -260 <= new_y <= 260 and 
                    not self.will_collide_with_self(enemy_snake, new_x, new_y)):
                    possible_directions.append("Right")
                
                # 如果有安全方向，随机选择一个
                if possible_directions:
                    # 尽量避免立即反向（如果可能的话）
                    current_direction = self.enemy_directions[idx]
                    reverse_directions = {"Up": "Down", "Down": "Up", "Left": "Right", "Right": "Left"}
                    
                    if current_direction in possible_directions and len(possible_directions) > 1:
                        # 移除反向方向（如果存在且不是唯一选择）
                        reverse_dir = reverse_directions[current_direction]
                        if reverse_dir in possible_directions:
                            possible_directions.remove(reverse_dir)
                    
                    self.enemy_directions[idx] = random.choice(possible_directions)
            
            # 移动整个蛇身
            for i in range(len(enemy_snake) - 1, 0, -1):
                if i-1 < len(enemy_snake) and i < len(enemy_snake):
                    x = enemy_snake[i-1].xcor()
                    y = enemy_snake[i-1].ycor()
                    enemy_snake[i].goto(x, y)
            
            # 移动头部
            current_direction = self.enemy_directions[idx]
            if current_direction == "Up":
                head.sety(head.ycor() + 20)
            elif current_direction == "Down":
                head.sety(head.ycor() - 20)
            elif current_direction == "Left":
                head.setx(head.xcor() - 20)
            elif current_direction == "Right":
                head.setx(head.xcor() + 20)
                
            # 检查是否撞墙，如果撞墙就强制转向
            x, y = head.position()
            if x <= -360 or x >= 360 or y <= -260 or y >= 260:
                # 撞墙了，立即转向
                possible_directions = []
                current_x, current_y = head.position()
                
                # 检查各个方向是否安全
                for test_dir in ["Up", "Down", "Left", "Right"]:
                    if test_dir == "Up":
                        test_x, test_y = current_x, current_y + 20
                    elif test_dir == "Down":
                        test_x, test_y = current_x, current_y - 20
                    elif test_dir == "Left":
                        test_x, test_y = current_x - 20, current_y
                    elif test_dir == "Right":
                        test_x, test_y = current_x + 20, current_y
                    
                    if (-360 <= test_x <= 360 and -260 <= test_y <= 260 and 
                        not self.will_collide_with_self(enemy_snake, test_x, test_y)):
                        possible_directions.append(test_dir)
                
                if possible_directions:
                    self.enemy_directions[idx] = random.choice(possible_directions)
                    # 立即移动到安全位置
                    new_direction = self.enemy_directions[idx]
                    if new_direction == "Up":
                        head.sety(current_y + 20)
                    elif new_direction == "Down":
                        head.sety(current_y - 20)
                    elif new_direction == "Left":
                        head.setx(current_x - 20)
                    elif new_direction == "Right":
                        head.setx(current_x + 20)

    def will_collide_with_self(self, enemy_snake, new_x, new_y):
        """检查移动到新位置是否会与自身重叠"""
        for segment in enemy_snake[1:]:  # 跳过头部
            if segment.distance(new_x, new_y) < 15:
                return True
        return False
        
    def create_bullet(self):
        """创建子弹 - 从蛇头发射"""
        if not self.game_started or self.is_dead:
            return
            
        head = self.snake[0]
        bullet = turtle.Turtle()
        bullet.shape("triangle")
        bullet.color("#FF4444")
        bullet.shapesize(0.3, 0.5)
        bullet.penup()
        bullet.goto(head.xcor(), head.ycor())
        
        # 设置子弹方向与蛇头方向一致
        if self.direction == "Up":
            bullet.setheading(90)
        elif self.direction == "Down":
            bullet.setheading(270)
        elif self.direction == "Left":
            bullet.setheading(180)
        elif self.direction == "Right":
            bullet.setheading(0)
            
        self.bullets.append(bullet)
        
    def move_bullets(self):
        """移动子弹并检测碰撞"""
        if not self.game_started or self.is_dead:
            return
            
        bullets_to_remove = []
        for bullet in self.bullets:
            bullet.forward(25)
            
            # 检查子弹是否击中围墙
            x, y = bullet.position()
            if x < -390 or x > 390 or y < -290 or y > 290:
                bullets_to_remove.append(bullet)
                continue
                
            # 检查子弹是否击中敌对蛇
            bullet_hit = False
            enemy_snakes_to_remove = []
            
            for idx, enemy_snake in enumerate(self.enemy_snakes[:]):
                for segment in enemy_snake:
                    if bullet.distance(segment) < 15:
                        # 击中敌对蛇 - 整条蛇消失
                        enemy_snakes_to_remove.append((idx, enemy_snake))
                        bullet_hit = True
                        
                        # 击中整条敌对蛇加111分
                        self.manager.add_score(111)
                        
                        # 为整条蛇创建爆炸特效
                        for seg in enemy_snake:
                            self.create_enemy_death_effect(seg.xcor(), seg.ycor())
                        
                        break
                # 如果击中了一条蛇，就不再检查这条蛇的其他段
                if bullet_hit:
                    break
                    
            # 移除被击中的整条蛇
            for idx, enemy_snake in enemy_snakes_to_remove:
                if enemy_snake in self.enemy_snakes:
                    # 隐藏所有蛇段
                    for segment in enemy_snake:
                        segment.hideturtle()
                    # 从敌对蛇列表中移除
                    self.enemy_snakes.remove(enemy_snake)
                    # 从方向列表中移除
                    if idx < len(self.enemy_directions):
                        del self.enemy_directions[idx]
                
            if bullet_hit:
                bullets_to_remove.append(bullet)
                continue
                
            # 检查子弹是否击中食物
            if bullet.distance(self.food) < 20:
                self.move_food()
                bullets_to_remove.append(bullet)
                continue
                    
        # 移除需要删除的子弹
        for bullet in bullets_to_remove:
            if bullet in self.bullets:
                bullet.hideturtle()
                self.bullets.remove(bullet)
                
    def create_enemy_death_effect(self, x, y):
        """创建敌对蛇死亡特效 - 灰色爆炸"""
        for _ in range(8):
            particle = turtle.Turtle()
            particle.shape("circle")
            particle.color("#808080")
            particle.penup()
            particle.goto(x, y)
            particle.shapesize(0.3, 0.3)
            
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(3, 8)
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed
            
            self.particles.append((particle, vx, vy))
            
    def update_particles(self):
        """更新粒子效果"""
        alive_particles = []
        
        for particle, vx, vy in self.particles:
            x, y = particle.position()
            particle.goto(x + vx, y + vy)
            
            # 添加重力效果
            vy -= 0.1
            
            # 粒子逐渐变小
            current_size = particle.shapesize()[0]
            if current_size > 0.05:
                particle.shapesize(current_size * 0.9, current_size * 0.9)
                alive_particles.append((particle, vx, vy))
            else:
                particle.hideturtle()
                
        self.particles = alive_particles
        
    def check_collision(self):
        """检查玩家碰撞"""
        if not self.game_started or self.is_dead:
            return False
            
        head = self.snake[0]
        
        # 检查围墙碰撞
        for wall in self.walls:
            if head.distance(wall) < 15:
                return True
                
        # 检查自身碰撞
        for segment in self.snake[1:]:
            if head.distance(segment) < 10:
                return True
                
        # 检查敌对蛇碰撞
        for enemy_snake in self.enemy_snakes:
            for segment in enemy_snake:
                if head.distance(segment) < 15:
                    return True
                    
        return False
        
    def check_food_collision(self):
        """检查食物碰撞"""
        if not self.game_started or self.is_dead:
            return False
            
        head = self.snake[0]
        
        if head.distance(self.food) < 20:
            self.manager.add_score(37)
            self.move_food()
            self.add_segment()
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
        
    def move(self):
        """移动蛇"""
        if not self.game_started or self.is_dead:
            return
            
        self.direction = self.next_direction
        
        # 移动身体段
        for i in range(len(self.snake) - 1, 0, -1):
            if i-1 < len(self.snake) and i < len(self.snake):
                x = self.snake[i-1].xcor()
                y = self.snake[i-1].ycor()
                self.snake[i].goto(x, y)
            
        # 移动头部
        head = self.snake[0]
        if self.direction == "Up":
            head.sety(head.ycor() + 20)
            head.setheading(90)
        elif self.direction == "Down":
            head.sety(head.ycor() - 20)
            head.setheading(270)
        elif self.direction == "Left":
            head.setx(head.xcor() - 20)
            head.setheading(180)
        elif self.direction == "Right":
            head.setx(head.xcor() + 20)
            head.setheading(0)
            
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
            
    def check_victory(self):
        """检查是否达到666分胜利"""
        return self.manager.current_game_score >= 666
        
    def create_death_effect(self, x, y):
        """创建玩家死亡特效"""
        for _ in range(15):
            particle = turtle.Turtle()
            particle.shape("circle")
            particle.color("#808080")
            particle.penup()
            particle.goto(x, y)
            particle.shapesize(0.5, 0.5)
            
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(2, 8)
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed
            
            self.particles.append((particle, vx, vy))
            
    def game_over_sequence(self):
        """游戏结束序列"""
        self.is_dead = True
        
        # 清除所有按键绑定
        self.screen.listen()
        self.screen.onkeypress(None, "Up")
        self.screen.onkeypress(None, "Down")
        self.screen.onkeypress(None, "Left")
        self.screen.onkeypress(None, "Right")
        self.screen.onkeypress(None, "space")
        
        # 玩家蛇逐渐变灰
        for i in range(10):
            for segment in self.snake:
                gray_value = int(255 * (i / 10))
                gray_hex = f"#{gray_value:02x}{gray_value:02x}{gray_value:02x}"
                segment.color(gray_hex)
            self.screen.update()
            time.sleep(0.05)
            
        # 创建爆炸粒子
        for segment in self.snake:
            x, y = segment.position()
            self.create_death_effect(x, y)
            segment.hideturtle()
            
        # 粒子爆炸效果
        for _ in range(30):
            self.update_particles()
            self.screen.update()
            time.sleep(0.05)
            
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
        self.death_animation_complete = True
        
        # 设置R键监听器
        self.screen.listen()
        self.screen.onkeypress(self.return_to_title, "r")
        self.screen.onkeypress(self.return_to_title, "R")
        
    def return_to_title(self):
        """返回标题"""
        if self.manager.session_total_score > self.manager.save_data.historical_total:
            self.manager.save_data.historical_total = self.manager.session_total_score
        from save_manager import SaveManager
        SaveManager.save_game(self.manager.save_data)
        
        self.manager.reset_game_score()
        self.manager.change_state(GameState.TITLE)
        
    def victory(self):
        """胜利"""
        victory_text = turtle.Turtle()
        victory_text.hideturtle()
        victory_text.penup()
        victory_text.color("red")
        victory_text.goto(0, 0)
        victory_text.write("VICTORY!", align="center", font=("Arial", 24, "bold"))
        
        score_text = turtle.Turtle()
        score_text.hideturtle()
        score_text.penup()
        score_text.color("white")
        score_text.goto(0, -50)
        score_text.write(f"Score: {self.manager.current_game_score}", align="center", 
                        font=("Arial", 16, "normal"))
        
        continue_text = turtle.Turtle()
        continue_text.hideturtle()
        continue_text.penup()
        continue_text.color("yellow")
        continue_text.goto(0, -100)
        continue_text.write("Loading next level...", align="center", font=("Arial", 16, "normal"))
        
        self.screen.update()
        
        # 保存当前进度
        if self.manager.session_total_score > self.manager.save_data.historical_total:
            self.manager.save_data.historical_total = self.manager.session_total_score
        from save_manager import SaveManager
        SaveManager.save_game(self.manager.save_data)
        
        # 2秒后进入下一个游戏
        time.sleep(0)
        self.manager.change_state(GameState.RED_BREAKOUT_INTRO)
        
    def cleanup(self):
        """清理游戏资源"""
        for segment in self.snake:
            segment.hideturtle()
        
        for enemy_snake in self.enemy_snakes:
            for segment in enemy_snake:
                segment.hideturtle()
        
        if self.food:
            self.food.hideturtle()
        
        for bullet in self.bullets:
            bullet.hideturtle()
        
        for particle, _, _ in self.particles:
            particle.hideturtle()
        
        for wall in self.walls:
            wall.hideturtle()
            
    def run(self):
        """运行红色贪吃蛇游戏"""
        self.reset_game_state()
        
        self.clear_screen()
        self.manager.score_display.update()
        
        # 创建游戏元素（直接开始）
        self.create_walls()
        self.create_player_snake()
        self.create_enemy_snakes()
        self.create_food()
        
        # 绑定按键
        self.screen.listen()
        self.screen.onkeypress(self.go_up, "Up")
        self.screen.onkeypress(self.go_down, "Down")
        self.screen.onkeypress(self.go_left, "Left")
        self.screen.onkeypress(self.go_right, "Right")
        self.screen.onkeypress(self.create_bullet, "space")
        self.screen.onkeypress(self.return_to_title, "r")
        self.screen.onkeypress(self.return_to_title, "R")
        
        # 游戏主循环
        while self.manager.current_state == GameState.RED_SNAKE:
            
            if not self.is_dead:
                # 游戏进行中
                self.move()
                self.move_enemy_snakes()
                self.move_bullets()
                self.update_particles()
                
                if self.check_collision():
                    self.game_over_sequence()
                    
                if self.check_food_collision():
                    # 检查胜利条件
                    if self.check_victory():
                        self.victory()
                        break
                        
            self.screen.update()
            time.sleep(0.1)
            
        # 游戏结束处理
        if self.is_dead:
            while self.manager.current_state == GameState.RED_SNAKE:
                self.screen.update()
                time.sleep(0.1)
        
        # 游戏结束后清理资源
        self.cleanup()