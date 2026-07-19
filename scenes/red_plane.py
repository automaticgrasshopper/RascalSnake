import turtle
import time
import random
import math
from scenes.base_scene import BaseScene
from constants import GameState

class RedPlane(BaseScene):
    def __init__(self, game_manager):
        super().__init__(game_manager)
        self.reset_game_state()
        
    def reset_game_state(self):
        """重置游戏状态"""
        self.player = None
        self.blue_enemies = []
        self.purple_enemies = []
        self.enemy_bullets = []
        self.player_bullets = []
        self.blue_killed = 0
        self.purple_killed = 0
        self.game_over = False
        self.game_started = True
        self.particles = []
        
        # 敌机消息
        self.blue_messages = [
            "No, disgusting! How could this be?",
            "So what father said is true!",
            "Don't kill me!"
        ]
        
        self.purple_messages = [
            "The mark on his head, that church...",
            "Put down your weapon, we can talk.",
            "Calm down, after all, we are..."
        ]
        
        # 帧率控制
        self.last_update_time = time.time()
        
    def create_player(self):
        """创建玩家飞机（白色）"""
        self.player = turtle.Turtle()
        self.player.shape("triangle")
        self.player.color("white")
        self.player.shapesize(1, 1)
        self.player.penup()
        self.player.goto(0, -200)
        self.player.setheading(90)  # 指向屏幕上方
        
    def create_enemies(self):
        """创建敌机（蓝色和紫色各3架）- 离玩家更近"""
        # 蓝色敌机位置 - 离玩家更近两个格子（向下移动40像素）
        blue_positions = [(-200, 160), (0, 210), (200, 160)]  # 原来y=200,250,200，现在减少40
        
        for pos in blue_positions:
            enemy = turtle.Turtle()
            enemy.shape("triangle")
            enemy.color("blue")
            enemy.shapesize(1, 1)
            enemy.penup()
            enemy.goto(pos[0], pos[1])
            enemy.setheading(270)  # 指向屏幕下方
            self.blue_enemies.append(enemy)
            
        # 紫色敌机位置 - 离玩家更近两个格子（向下移动40像素）
        purple_positions = [(-150, 110), (150, 110), (0, 260)]  # 原来y=150,150,300，现在减少40
        
        for pos in purple_positions:
            enemy = turtle.Turtle()
            enemy.shape("triangle")
            enemy.color("#8A2BE2")  # 紫色
            enemy.shapesize(1, 1)
            enemy.penup()
            enemy.goto(pos[0], pos[1])
            enemy.setheading(270)
            self.purple_enemies.append(enemy)
            
    def move_enemies(self):
        """移动敌机"""
        # 移动蓝色敌机
        for enemy in self.blue_enemies[:]:
            # 随机移动
            if random.random() < 0.02:
                enemy.setx(enemy.xcor() + random.randint(-20, 20))
                
            # 边界检查
            if enemy.xcor() > 350:
                enemy.setx(350)
            elif enemy.xcor() < -350:
                enemy.setx(-350)
                
            # 检查与玩家碰撞
            if self.player and self.player.distance(enemy) < 20:
                self.plane_death_animation()
                return
                
        # 移动紫色敌机
        for enemy in self.purple_enemies[:]:
            # 随机移动
            if random.random() < 0.02:
                enemy.setx(enemy.xcor() + random.randint(-20, 20))
                
            # 边界检查
            if enemy.xcor() > 350:
                enemy.setx(350)
            elif enemy.xcor() < -350:
                enemy.setx(-350)
                
            # 检查与玩家碰撞
            if self.player and self.player.distance(enemy) < 20:
                self.plane_death_animation()
                return
                
    def create_enemy_bullet(self):
        """敌机发射子弹（红色）- 提高攻击频率"""
        # 蓝色敌机发射 - 提高频率
        if self.blue_enemies and random.random() < 0.04:  # 从0.02提高到0.04
            enemy = random.choice(self.blue_enemies)
            bullet = turtle.Turtle()
            bullet.shape("circle")
            bullet.color("red")
            bullet.shapesize(0.3, 0.3)
            bullet.penup()
            bullet.goto(enemy.xcor(), enemy.ycor() - 20)
            self.enemy_bullets.append(bullet)
            
        # 紫色敌机发射 - 提高频率
        if self.purple_enemies and random.random() < 0.04:  # 从0.02提高到0.04
            enemy = random.choice(self.purple_enemies)
            bullet = turtle.Turtle()
            bullet.shape("circle")
            bullet.color("red")
            bullet.shapesize(0.3, 0.3)
            bullet.penup()
            bullet.goto(enemy.xcor(), enemy.ycor() - 20)
            self.enemy_bullets.append(bullet)
            
    def move_enemy_bullets(self):
        """移动敌机子弹"""
        bullets_to_remove = []
        
        for bullet in self.enemy_bullets:
            bullet.sety(bullet.ycor() - 8)  # 向下移动
            
            # 检查是否击中玩家
            if self.player and bullet.distance(self.player) < 20:
                bullets_to_remove.append(bullet)
                self.plane_death_animation()
                break
                
            # 检查是否飞出屏幕底部
            if bullet.ycor() < -300:
                bullets_to_remove.append(bullet)
                
        # 移除需要删除的子弹
        for bullet in bullets_to_remove:
            if bullet in self.enemy_bullets:
                bullet.hideturtle()
                self.enemy_bullets.remove(bullet)
                
    def create_player_bullet(self):
        """玩家发射子弹"""
        if not self.game_started or self.game_over:
            return
            
        bullet = turtle.Turtle()
        bullet.shape("circle")
        bullet.color("white")
        bullet.shapesize(0.3, 0.3)
        bullet.penup()
        bullet.goto(self.player.xcor(), self.player.ycor() + 20)
        self.player_bullets.append(bullet)
        
    def move_player_bullets(self):
        """移动玩家子弹"""
        bullets_to_remove = []
        
        for bullet in self.player_bullets:
            bullet.sety(bullet.ycor() + 10)  # 向上移动
            
            # 检查是否飞出屏幕顶部
            if bullet.ycor() > 300:
                bullets_to_remove.append(bullet)
                continue
                
            # 检查子弹与蓝色敌机碰撞
            for enemy in self.blue_enemies[:]:
                if bullet.distance(enemy) < 20:
                    # 击中蓝色敌机
                    bullets_to_remove.append(bullet)
                    
                    enemy.hideturtle()
                    self.blue_enemies.remove(enemy)
                    
                    # 增加分数
                    self.manager.add_score(150)
                    self.blue_killed += 1
                    
                    # 显示蓝色消息
                    self.show_message(self.blue_messages[self.blue_killed - 1], "blue")
                    break
                    
            if bullet in bullets_to_remove:
                continue
                
            # 检查子弹与紫色敌机碰撞
            for enemy in self.purple_enemies[:]:
                if bullet.distance(enemy) < 20:
                    # 击中紫色敌机
                    bullets_to_remove.append(bullet)
                    
                    enemy.hideturtle()
                    self.purple_enemies.remove(enemy)
                    
                    # 增加分数
                    self.manager.add_score(150)
                    self.purple_killed += 1
                    
                    # 显示紫色消息
                    self.show_message(self.purple_messages[self.purple_killed - 1], "#8A2BE2")
                    break
                    
        # 移除需要删除的子弹
        for bullet in bullets_to_remove:
            if bullet in self.player_bullets:
                bullet.hideturtle()
                self.player_bullets.remove(bullet)
                
    def show_message(self, message, color):
        """显示击杀消息"""
        message_turtle = turtle.Turtle()
        message_turtle.hideturtle()
        message_turtle.penup()
        message_turtle.color(color)
        message_turtle.goto(0, 250)
        message_turtle.write(message, align="center", font=("Arial", 14, "normal"))
        
        # 2秒后清除消息
        self.screen.ontimer(lambda: message_turtle.clear(), 2000)
        
    def move_left(self):
        """玩家向左移动"""
        if not self.game_started or self.game_over:
            return
            
        x = self.player.xcor()
        if x > -350:
            self.player.setx(x - 20)
            
    def move_right(self):
        """玩家向右移动"""
        if not self.game_started or self.game_over:
            return
            
        x = self.player.xcor()
        if x < 350:
            self.player.setx(x + 20)
            
    def check_victory(self):
        """检查是否完成6个敌机的击杀"""
        return self.blue_killed >= 3 and self.purple_killed >= 3
        
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
        
    def plane_death_animation(self):
        """飞机死亡动画"""
        self.game_over = True
        
        # 清除所有按键绑定
        self.screen.listen()
        self.screen.onkeypress(None, "Left")
        self.screen.onkeypress(None, "Right")
        self.screen.onkeypress(None, "space")
        
        # 玩家飞机逐渐变灰
        for i in range(10):
            gray_value = int(255 * (i / 10))
            gray_hex = f"#{gray_value:02x}{gray_value:02x}{gray_value:02x}"
            self.player.color(gray_hex)
            self.screen.update()
            time.sleep(0.05)
            
        # 创建爆炸粒子
        x, y = self.player.position()
        for _ in range(15):
            particle, vx, vy = self.create_particle(x, y)
            self.particles.append((particle, vx, vy))
        self.player.hideturtle()
        
        # 清除敌机和子弹
        for enemy in self.blue_enemies + self.purple_enemies:
            enemy.hideturtle()
        for bullet in self.player_bullets + self.enemy_bullets:
            bullet.hideturtle()
            
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
        
        # 设置R键监听器
        self.screen.listen()
        self.screen.onkeypress(self.return_to_title, "r")
        self.screen.onkeypress(self.return_to_title, "R")
        
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
        score_text.write(f"Blue: {self.blue_killed}/3 | Purple: {self.purple_killed}/3", 
                        align="center", font=("Arial", 16, "normal"))
        
        continue_text = turtle.Turtle()
        continue_text.hideturtle()
        continue_text.penup()
        continue_text.color("yellow")
        continue_text.goto(0, -100)
        continue_text.write("Loading...", align="center", font=("Arial", 16, "normal"))
        
        self.screen.update()
        
        # 保存分数
        if self.manager.session_total_score > self.manager.save_data.historical_total:
            self.manager.save_data.historical_total = self.manager.session_total_score
        from save_manager import SaveManager
        SaveManager.save_game(self.manager.save_data)
        
        # 2秒后进入下一个游戏
        time.sleep(0)
        self.manager.change_state(GameState.RED_QTE_INTRO)
        
    def return_to_title(self):
        """返回标题"""
        # 保存当前历史最高分
        if self.manager.session_total_score > self.manager.save_data.historical_total:
            self.manager.save_data.historical_total = self.manager.session_total_score
        from save_manager import SaveManager
        SaveManager.save_game(self.manager.save_data)
        
        self.manager.reset_game_score()
        self.manager.change_state(GameState.TITLE)
        
    def cleanup(self):
        """清理游戏资源"""
        # 隐藏所有元素
        if self.player:
            self.player.hideturtle()
            
        for enemy in self.blue_enemies + self.purple_enemies:
            enemy.hideturtle()
            
        for bullet in self.player_bullets + self.enemy_bullets:
            bullet.hideturtle()
            
        for particle, _, _ in self.particles:
            particle.hideturtle()
        
    def run(self):
        """运行红色飞机游戏"""
        # 重置状态
        self.reset_game_state()
        
        self.clear_screen()
        self.manager.score_display.update()
        
        # 创建游戏元素
        self.create_player()
        self.create_enemies()
        
        # 绑定按键
        self.screen.listen()
        self.screen.onkeypress(self.move_left, "Left")
        self.screen.onkeypress(self.move_right, "Right")
        self.screen.onkeypress(self.create_player_bullet, "space")
        self.screen.onkeypress(self.return_to_title, "r")
        self.screen.onkeypress(self.return_to_title, "R")
        
        # 性能优化：帧率控制
        target_fps = 60
        frame_delay = 1.0 / target_fps
        last_time = time.time()
        
        # 敌机发射计时器
        enemy_shoot_timer = 0
        
        # 游戏主循环
        while (self.manager.current_state == GameState.RED_PLANE and 
               not self.game_over and not self.check_victory()):
            
            current_time = time.time()
            delta_time = current_time - last_time
            
            # 帧率控制
            if delta_time < frame_delay:
                time.sleep(frame_delay - delta_time)
                
            last_time = time.time()
            
            # 更新游戏状态
            self.move_enemies()
            self.move_player_bullets()
            
            # 敌机发射子弹 - 提高频率
            enemy_shoot_timer += 1
            if enemy_shoot_timer >= 15:  # 从30帧减少到20帧，提高发射频率
                self.create_enemy_bullet()
                enemy_shoot_timer = 0
                
            self.move_enemy_bullets()
            
            # 检查胜利条件
            if self.check_victory():
                self.victory()
                break
                
            self.screen.update()
            
        # 游戏结束处理
        if self.game_over:
            while self.manager.current_state == GameState.RED_PLANE and self.game_over:
                current_time = time.time()
                delta_time = current_time - last_time
                
                # 帧率控制
                if delta_time < frame_delay:
                    time.sleep(frame_delay - delta_time)
                    
                last_time = time.time()
                self.screen.update()
        
        # 清理资源
        self.cleanup()