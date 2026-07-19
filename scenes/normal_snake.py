import turtle
import time
import random
import math
from scenes.base_scene import BaseScene
from constants import GameState

class NormalSnake(BaseScene):
    def __init__(self, game_manager):
        super().__init__(game_manager)
        self.reset_game_state()
        
    def reset_game_state(self):
        """重置游戏状态"""
        self.snake = []
        self.foods = []  # 三种颜色食物
        self.walls = []
        self.enemies = []  # 敌机
        self.enemy_bullets = []  # 敌机子弹
        self.player_bullets = []  # 玩家子弹
        self.direction = "Right"
        self.next_direction = "Right"
        self.is_dead = False
        self.game_started = True  # 直接开始游戏
        self.current_color = "red"  # 当前蛇的颜色（初始为红色）
        self.particles = []  # 用于死亡动画的粒子
        self.death_animation_complete = False
        self.enemy_spawn_timer = 0
        self.enemy_shoot_timer = 0
        self.snake_speed = 3  # 蛇模式移动速度（帧数控制）
        self.move_counter = 0
        
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
        
    def create_snake(self):
        """创建三色渐变蛇，从中心开始，尖尖的头"""
        start_x, start_y = 0, 0
        
        # 定义三种基础颜色：红、蓝、紫
        base_colors = ["#FF0000", "#0000FF", "#8A2BE2"]  # 红、蓝、紫
        
        for i in range(3):
            segment = turtle.Turtle()
            
            # 三色渐变：红->蓝->紫
            color_index = i % 3
            current_color = base_colors[color_index]
            
            if i == 0:  # 蛇头 - 三角形
                segment.shape("triangle")
                segment.color(current_color)  # 头部使用基础颜色
            else:  # 蛇身使用对应颜色的渐变
                # 根据位置计算颜色强度
                intensity = max(100, 255 - i * 40)  # 身体颜色逐渐变淡
                if color_index == 0:  # 红色
                    segment.color(f"#{intensity:02x}0000")
                elif color_index == 1:  # 蓝色
                    segment.color(f"#0000{intensity:02x}")
                else:  # 紫色
                    red_intensity = max(80, intensity - 40)
                    blue_intensity = max(120, intensity - 20)
                    segment.color(f"#{red_intensity:02x}00{blue_intensity:02x}")
                segment.shape("square")
                
            segment.penup()
            segment_x = start_x - i * 20
            segment_y = start_y
            segment.goto(segment_x, segment_y)
            self.snake.append(segment)
            
    def apply_rascal_effect(self):
        """应用赖皮效果 - 蛇身轻微扭动"""
        for i, segment in enumerate(self.snake):
            if i > 0:  # 蛇头不动，身体段轻微移动
                current_x, current_y = segment.position()
                # 轻微的随机偏移，制造赖皮扭动效果
                new_x = current_x + random.randint(-1, 1)
                new_y = current_y + random.randint(-1, 1)
                
                # 确保不会移动到围墙外
                if -360 <= new_x <= 360 and -260 <= new_y <= 260:
                    segment.goto(new_x, new_y)
                    
    def create_foods(self):
        """创建三种颜色食物（紫色、红色、蓝色）"""
        colors = ["#8A2BE2", "#FF0000", "#0000FF"]  # 紫色、红色、蓝色
        
        for color in colors:
            food = turtle.Turtle()
            food.shape("circle")
            food.color(color)
            food.penup()
            self.move_food(food)
            self.foods.append(food)
        
    def move_food(self, food):
        """移动食物到随机位置"""
        while True:
            x = (random.randint(-17, 17) * 20)
            y = (random.randint(-12, 12) * 20)
            if (-360 <= x <= 360 and -260 <= y <= 260):
                food.goto(x, y)
                break
                
    def create_enemy(self):
        """创建敌机 - 在角落随机生成"""
        if len(self.enemies) < 2:  # 限制最多2个敌机
            enemy = turtle.Turtle()
            enemy.shape("triangle")
            enemy.color("white")
            enemy.shapesize(0.8, 0.8)
            enemy.penup()
            
            # 在四个角落之一生成
            corners = [(-350, 250), (350, 250), (-350, -250), (350, -250)]
            start_x, start_y = random.choice(corners)
            enemy.goto(start_x, start_y)
            
            # 随机方向
            directions = ["Up", "Down", "Left", "Right"]
            enemy.direction = random.choice(directions)
            
            self.enemies.append(enemy)
            
    def move_enemies(self):
        """移动敌机 - 随机自由移动"""
        for enemy in self.enemies[:]:
            # 根据方向移动
            if enemy.direction == "Up":
                enemy.sety(enemy.ycor() + 5)
            elif enemy.direction == "Down":
                enemy.sety(enemy.ycor() - 5)
            elif enemy.direction == "Left":
                enemy.setx(enemy.xcor() - 5)
            elif enemy.direction == "Right":
                enemy.setx(enemy.xcor() + 5)
                
            # 边界检查，碰到边界就转向
            x, y = enemy.position()
            if x <= -360 or x >= 360 or y <= -260 or y >= 260:
                # 随机选择新方向
                directions = ["Up", "Down", "Left", "Right"]
                enemy.direction = random.choice(directions)
                
            # 检查敌机与玩家碰撞
            head = self.snake[0]
            if head.distance(enemy) < 20:
                self.game_over()
                return
                
    def create_enemy_bullet(self):
        """敌机发射子弹 - 改为固定方向发射"""
        if not self.enemies:
            return
            
        # 随机选择一个敌机发射
        enemy = random.choice(self.enemies)
        bullet = turtle.Turtle()
        bullet.shape("circle")
        bullet.color("red")
        bullet.shapesize(0.3, 0.3)
        bullet.penup()
        bullet.goto(enemy.xcor(), enemy.ycor())
        
        # 设置子弹方向为敌机的当前方向
        bullet.direction = enemy.direction
        self.enemy_bullets.append(bullet)
        
    def move_enemy_bullets(self):
        """移动敌机子弹 - 改为固定方向移动"""
        bullets_to_remove = []
        
        for bullet in self.enemy_bullets:
            # 根据子弹的固定方向移动
            if bullet.direction == "Up":
                bullet.sety(bullet.ycor() + 8)
            elif bullet.direction == "Down":
                bullet.sety(bullet.ycor() - 8)
            elif bullet.direction == "Left":
                bullet.setx(bullet.xcor() - 8)
            elif bullet.direction == "Right":
                bullet.setx(bullet.xcor() + 8)
                
            # 检查是否击中玩家
            head = self.snake[0]
            if head.distance(bullet) < 20:
                bullets_to_remove.append(bullet)
                self.game_over()
                break
                
            # 检查是否飞出屏幕
            if (bullet.xcor() < -400 or bullet.xcor() > 400 or 
                bullet.ycor() < -300 or bullet.ycor() > 300):
                bullets_to_remove.append(bullet)
                
        # 移除需要删除的子弹
        for bullet in bullets_to_remove:
            if bullet in self.enemy_bullets:
                bullet.hideturtle()
                self.enemy_bullets.remove(bullet)
                
    def create_player_bullet(self):
        """玩家发射子弹 - 从蛇头发射"""
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
            
        self.player_bullets.append(bullet)
        
    def move_player_bullets(self):
        """移动玩家子弹并检测碰撞"""
        if not self.game_started or self.is_dead:
            return
            
        bullets_to_remove = []
        for bullet in self.player_bullets:
            bullet.forward(20)
            
            # 检查子弹是否击中围墙
            x, y = bullet.position()
            if x < -390 or x > 390 or y < -290 or y > 290:
                bullets_to_remove.append(bullet)
                continue
                
            # 检查子弹是否击中敌机
            bullet_hit = False
            for enemy in self.enemies[:]:
                if bullet.distance(enemy) < 20:
                    # 击中敌机
                    enemy.hideturtle()
                    self.enemies.remove(enemy)
                    bullets_to_remove.append(bullet)
                    bullet_hit = True
                    
                    # 击中敌机加50分
                    self.manager.add_score(50)
                    break
                    
            if bullet_hit:
                continue
                    
        # 移除需要删除的子弹
        for bullet in bullets_to_remove:
            if bullet in self.player_bullets:
                bullet.hideturtle()
                self.player_bullets.remove(bullet)
                
    def check_collision(self):
        """检查碰撞"""
        head = self.snake[0]
        
        # 检查围墙碰撞
        for wall in self.walls:
            if head.distance(wall) < 15:
                return True
                
        # 检查自身碰撞
        for segment in self.snake[1:]:
            if head.distance(segment) < 10:
                return True
                
        return False
        
    def check_food_collision(self):
        """检查食物碰撞并改变蛇颜色"""
        head = self.snake[0]
        
        for food in self.foods:
            if head.distance(food) < 20:
                # 根据食物颜色改变蛇颜色（只改变第4节及以后的身体）
                food_color = food.color()[0]  # 获取食物颜色
                self.change_snake_color(food_color)
                
                self.manager.add_score(37)  # 每个食物37分
                self.move_food(food)
                self.add_segment()
                return True
                
        return False
        
    def change_snake_color(self, color):
        """改变蛇的颜色（只改变第4节及以后的身体）"""
        self.current_color = color
        
        # 定义三种基础颜色：红、蓝、紫
        base_colors = ["#FF0000", "#0000FF", "#8A2BE2"]  # 红、蓝、紫
        
        # 只改变第4节及以后的身体颜色
        for i, segment in enumerate(self.snake):
            if i >= 4:  # 第4节及以后
                color_index = i % 3  # 红蓝紫循环
                intensity = max(80, 255 - (i - 4) * 25)  # 颜色逐渐变淡
                
                if color_index == 0:  # 红色
                    segment.color(f"#{intensity:02x}0000")
                elif color_index == 1:  # 蓝色
                    segment.color(f"#0000{intensity:02x}")
                else:  # 紫色
                    red_intensity = max(60, intensity - 50)
                    blue_intensity = max(100, intensity - 30)
                    segment.color(f"#{red_intensity:02x}00{blue_intensity:02x}")
        
    def add_segment(self):
        """添加蛇身段 - 使用三色渐变"""
        segment = turtle.Turtle()
        segment.shape("square")
        
        # 根据当前颜色和位置决定新段的颜色
        i = len(self.snake)  # 新段的索引
        color_index = i % 3  # 红蓝紫循环
        intensity = max(80, 255 - (i - 3) * 25)  # 颜色逐渐变淡
        
        if color_index == 0:  # 红色
            segment.color(f"#{intensity:02x}0000")
        elif color_index == 1:  # 蓝色
            segment.color(f"#0000{intensity:02x}")
        else:  # 紫色
            red_intensity = max(60, intensity - 50)
            blue_intensity = max(100, intensity - 30)
            segment.color(f"#{red_intensity:02x}00{blue_intensity:02x}")
        
        segment.penup()
        last_segment = self.snake[-1]
        segment.goto(last_segment.xcor(), last_segment.ycor())
        self.snake.append(segment)
        
    def move(self):
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
            
        # 应用赖皮效果
        self.apply_rascal_effect()
            
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
            
    def create_particle(self, x, y):
        """创建爆炸粒子"""
        particle = turtle.Turtle()
        particle.shape("circle")
        particle.color("#808080")  # 灰色
        particle.penup()
        particle.goto(x, y)
        particle.shapesize(0.5, 0.5)
        
        # 随机速度和方向
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(2, 8)
        vx = math.cos(angle) * speed
        vy = math.sin(angle) * speed
        
        return particle, vx, vy
        
    def death_animation(self):
        """死亡动画 - 灰色烟花爆炸"""
        self.is_dead = True
        
        # 清除所有按键绑定
        self.screen.listen()
        self.screen.onkeypress(None, "Up")
        self.screen.onkeypress(None, "Down")
        self.screen.onkeypress(None, "Left")
        self.screen.onkeypress(None, "Right")
        self.screen.onkeypress(None, "space")
        
        # 蛇身逐渐变灰
        for i in range(10):
            for segment in self.snake:
                # 计算灰度值 (0-255)
                gray_value = int(255 * (i / 10))
                gray_hex = f"#{gray_value:02x}{gray_value:02x}{gray_value:02x}"
                segment.color(gray_hex)
            self.screen.update()
            time.sleep(0.05)
            
        # 创建爆炸粒子
        for segment in self.snake:
            x, y = segment.position()
            # 每个蛇段创建多个粒子
            for _ in range(5):
                particle, vx, vy = self.create_particle(x, y)
                self.particles.append((particle, vx, vy))
            segment.hideturtle()
            
        # 隐藏敌机和子弹
        for enemy in self.enemies:
            enemy.hideturtle()
        for bullet in self.player_bullets + self.enemy_bullets:
            bullet.hideturtle()
        for food in self.foods:
            food.hideturtle()
        for wall in self.walls:
            wall.hideturtle()
            
        # 粒子爆炸效果
        for _ in range(30):  # 30帧爆炸动画
            for i, (particle, vx, vy) in enumerate(self.particles):
                x, y = particle.position()
                particle.goto(x + vx, y + vy)
                
                # 添加重力效果
                vy -= 0.2
                self.particles[i] = (particle, vx, vy)
                
                # 粒子逐渐变小
                current_size = particle.shapesize()[0]
                if current_size > 0.1:
                    particle.shapesize(current_size * 0.95, current_size * 0.95)
                    
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
        
    def check_victory(self):
        """检查是否达到666分胜利"""
        return self.manager.current_game_score >= 6666
        
    def game_over(self):
        """游戏结束"""
        self.death_animation()
        
        # 等待玩家按R键
        while self.is_dead and self.manager.current_state == GameState.NORMAL_SNAKE:
            self.screen.update()
            time.sleep(0.1)
            
    def victory(self):
        """胜利 - 显示红色艺术字和感谢信息"""
        # 清除屏幕
        self.clear_screen()
        
        # 显示红色ASCII艺术字
        art_turtle = turtle.Turtle()
        art_turtle.hideturtle()
        art_turtle.penup()
        art_turtle.color("red")
        
        ascii_art = [
            "                      :::!~!!!!!:.                  ",
            "                  .xUHWH!! !!?M88WHX:.              ",
            "                .X*#M@$!!  !X!M$$$$$$WWx:.          ",
            "               :!!!!!!?H! :!$!$$$$$$$$$$8X:         ",
            "              !!~  ~:~!! :~!$!#$$$$$$$$$$8X:        ",
            "             :!~::!H!<   ~.U$X!?R$$$$$$$$MM!        ",
            "             ~!~!!!!~~ .:XW$$$U!!?$$$$$$RMM!        ",
            "               !:~~~ .:!M\"T#$$$$WX??#MRRMMM!        ",
            "               ~?WuxiW*`   `\"#$$$$8!!!!??!!!        ",
            "             :X- M$$$$       `\"T#$T~!8$WUXU~        ",
            "            :%`  ~#$$$m:        ~!~ ?$$$$$$         ",
            "          :!`.-   ~T$$$$8xx.  .xWW- ~\"\"##*\"         ",
            ".....   -~~:<` !    ~?T#$$@@W@*?$$      /`          ",
            "W$@@M!!! .!~~ !!     .:XUW$W!~ `\"~:    :            ",
            "W$@@M!!! .!~~ !!     .:XUW$W!~ `\"~:    :            ",
            "#\"~~`.:x%`!!  !H:   !WM$$$$Ti.: .!WUn+!`            ",
            ":::~:!!`:X~ .: ?H.!u \"$$$B$$$!W:U!T$$M~             ",
            ".~~   :X@!.-~   ?@WTWo(\"*$$$W$TH$! `                ",
            "Wi.~!X$?!-~    : ?$$$B$Wu(\"**$RM!                   ",
            "$R@i.~~ !     :   ~$$$$$B$$en:``                    ",
            "?MXT@Wx.~    :     ~\"##*$$$$M~                      "
        ]
        
        for i, line in enumerate(ascii_art):
            art_turtle.goto(-380, 200 - i * 20)
            art_turtle.write(line, align="left", font=("Courier", 8, "normal"))
        
        # 显示感谢信息
        thank_you = turtle.Turtle()
        thank_you.hideturtle()
        thank_you.penup()
        thank_you.color("red")
        thank_you.goto(0, -200)
        thank_you.write("You have been registered. See you!", align="center", font=("Arial", 24, "bold"))
        
        continue_prompt = turtle.Turtle()
        continue_prompt.hideturtle()
        continue_prompt.penup()
        continue_prompt.color("yellow")
        continue_prompt.goto(0, -250)
        continue_prompt.write("Press R to return to Title", align="center", font=("Arial", 16, "normal"))
        
        self.screen.update()
        
        # 绑定按键 - 改为R键返回标题
        self.screen.listen()
        self.screen.onkeypress(self.return_to_title, "r")
        self.screen.onkeypress(self.return_to_title, "R")
        
        # 等待玩家按R键
        while self.manager.current_state == GameState.NORMAL_SNAKE:
            self.screen.update()
            time.sleep(0.1)
        
    def return_to_title(self):
        """返回标题"""
        # 重置游戏状态
        self.reset_game_state()
        self.manager.reset_game_score()
        self.manager.change_state(GameState.TITLE)
        
    def cleanup(self):
        """清理所有游戏元素"""
        # 隐藏所有蛇段
        for segment in self.snake:
            segment.hideturtle()
        
        # 隐藏所有食物
        for food in self.foods:
            food.hideturtle()
            
        # 隐藏所有敌机
        for enemy in self.enemies:
            enemy.hideturtle()
            
        # 隐藏所有子弹
        for bullet in self.player_bullets + self.enemy_bullets:
            bullet.hideturtle()
            
        # 隐藏所有围墙
        for wall in self.walls:
            wall.hideturtle()
            
        # 隐藏所有粒子
        for particle, _, _ in self.particles:
            particle.hideturtle()
            
        # 清空所有列表
        self.snake.clear()
        self.foods.clear()
        self.enemies.clear()
        self.player_bullets.clear()
        self.enemy_bullets.clear()
        self.walls.clear()
        self.particles.clear()
        
    def run(self):
        """运行普通贪吃蛇游戏"""
        # 每次运行时重置游戏状态
        self.reset_game_state()
        
        self.clear_screen()
        self.manager.score_display.update()
        
        # 创建游戏元素（直接开始）
        self.create_walls()
        self.create_snake()
        self.create_foods()
        
        # 绑定按键
        self.screen.listen()
        self.screen.onkeypress(self.go_up, "Up")
        self.screen.onkeypress(self.go_down, "Down")
        self.screen.onkeypress(self.go_left, "Left")
        self.screen.onkeypress(self.go_right, "Right")
        self.screen.onkeypress(self.create_player_bullet, "space")  # 空格发射子弹
        self.screen.onkeypress(self.return_to_title, "r")
        self.screen.onkeypress(self.return_to_title, "R")
        
        # 游戏主循环
        while self.manager.current_state == GameState.NORMAL_SNAKE and not self.is_dead:
            
            # 游戏进行中
            self.move()
            
            # 更新敌机系统
            self.enemy_spawn_timer += 1
            if self.enemy_spawn_timer >= 180:  # 每180帧生成一个敌机
                self.create_enemy()
                self.enemy_spawn_timer = 0
                
            self.move_enemies()
            
            # 敌机发射子弹
            self.enemy_shoot_timer += 1
            if self.enemy_shoot_timer >= 120:  # 每120帧发射一次
                self.create_enemy_bullet()
                self.enemy_shoot_timer = 0
                
            self.move_enemy_bullets()
            self.move_player_bullets()
            
            if self.check_collision():
                self.game_over()
                
            if self.check_food_collision():
                # 检查胜利条件
                if self.check_victory():
                    self.victory()
                    break
                        
            self.screen.update()
            time.sleep(0.016)  # 约60帧
            
        # 游戏结束处理
        if self.is_dead:
            while self.manager.current_state == GameState.NORMAL_SNAKE:
                self.screen.update()
                time.sleep(0.1)
        
        # 游戏结束后清理资源
        self.cleanup()