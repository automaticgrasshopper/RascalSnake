import turtle
import time
import random
import math
from scenes.base_scene import BaseScene
from constants import GameState, PLANE_ENEMY_POINTS, PLANE_ENEMY_COUNT

class BluePlane(BaseScene):
    def __init__(self, game_manager):
        super().__init__(game_manager)
        self.player = None
        self.enemies = []
        self.bullets = []
        self.enemies_killed = 0
        self.current_message_index = 0
        self.game_over = False
        self.game_started = False
        self.particles = []  # 用于死亡动画的粒子
        
    def create_blue_spiral(self):
        """创建蓝色蛇蜷缩成回字形的动画 - 类似打砖块进入效果"""
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
        
        # 蓝色方块充满屏幕
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
        
        # 蓝色方块缩小成飞机
        for size in range(500, 0, -15):
            blue_square.clear()
            if size > 0:
                blue_square.dot(size)
            self.screen.update()
            time.sleep(0.02)
        
        # 清除蓝色方块和蛇身段
        blue_square.hideturtle()
        for segment in segments:
            segment.hideturtle()
            
    def show_training_ground_title(self):
        """显示训练场标题 - 使用填充式艺术字"""
        # 清除屏幕
        self.clear_screen()
        
        # 显示填充式TRAINING GROUND艺术字
        title_turtle = turtle.Turtle()
        title_turtle.hideturtle()
        title_turtle.penup()
        
        # 填充式艺术字 - 使用实心字符
        training_art = [
            "▓▓▓▓▓▓▓▓▓▓  ▓▓▓▓▓▓▓▓▓▓   ▓▓▓▓▓▓▓▓▓▓▓▓  ▓▓▓▓▓▓▓▓▓▓  ▓▓▓▓▓▓▓▓▓▓   ▓▓▓▓▓▓▓▓▓▓▓▓ ▓▓▓▓▓▓▓▓▓▓▓▓ ▓▓▓▓▓▓▓▓▓▓▓▓ ▓▓▓▓▓▓▓▓▓▓▓▓",
            "▓▓▓▓▓▓▓▓▓▓ ▓▓▓▓▓▓▓▓▓▓▓▓  ▓▓▓▓▓▓▓▓▓▓▓▓ ▓▓▓▓▓▓▓▓▓▓▓ ▓▓▓▓▓▓▓▓▓▓▓▓  ▓▓▓▓▓▓▓▓▓▓▓▓ ▓▓▓▓▓▓▓▓▓▓▓▓ ▓▓▓▓▓▓▓▓▓▓▓▓ ▓▓▓▓▓▓▓▓▓▓▓▓",
            "   ▓▓▓▓    ▓▓▓▓    ▓▓▓▓▓     ▓▓▓▓     ▓▓▓▓   ▓▓▓▓ ▓▓▓▓    ▓▓▓▓▓     ▓▓▓▓     ▓▓▓▓         ▓▓▓▓         ▓▓▓▓        ",
            "   ▓▓▓▓    ▓▓▓▓     ▓▓▓▓     ▓▓▓▓     ▓▓▓▓▓▓▓▓▓▓▓ ▓▓▓▓     ▓▓▓▓     ▓▓▓▓     ▓▓▓▓▓▓▓▓     ▓▓▓▓▓▓▓      ▓▓▓▓▓▓▓▓    ",
            "   ▓▓▓▓    ▓▓▓▓      ▓▓▓     ▓▓▓▓     ▓▓▓▓   ▓▓▓▓ ▓▓▓▓      ▓▓▓     ▓▓▓▓     ▓▓▓▓         ▓▓▓▓         ▓▓▓▓        ",
            "   ▓▓▓▓    ▓▓▓▓       ▓▓▓    ▓▓▓▓     ▓▓▓▓   ▓▓▓▓ ▓▓▓▓       ▓▓▓    ▓▓▓▓     ▓▓▓▓▓▓▓▓▓▓▓  ▓▓▓▓▓▓▓▓▓▓▓  ▓▓▓▓▓▓▓▓▓▓▓ "
        ]
        
        # 绘制填充艺术字
        title_turtle.color("red")
        for i, line in enumerate(training_art):
            title_turtle.goto(-380, 150 - i * 20)
            title_turtle.write(line, align="left", font=("Courier", 8, "normal"))
        
        # 副标题
        subtitle = turtle.Turtle()
        subtitle.hideturtle()
        subtitle.penup()
        subtitle.color("white")
        subtitle.goto(0, -50)
        subtitle.write("TRAINING GROUND", align="center", font=("Arial", 20, "bold"))
        
        # 开始提示
        prompt = turtle.Turtle()
        prompt.hideturtle()
        prompt.penup()
        prompt.color("white")
        prompt.goto(0, -100)
        prompt.write("Press SPACE to start", align="center", font=("Arial", 16, "normal"))
        
        self.screen.update()
        
    def create_player(self):
        """创建玩家飞机（蓝色三角）"""
        self.player = turtle.Turtle()
        self.player.shape("triangle")
        self.player.color("blue")
        self.player.shapesize(1, 1)
        self.player.penup()
        self.player.goto(0, -200)
        self.player.setheading(90)  # 指向屏幕上方
        
    def create_enemy(self):
        """创建敌机（白色三角）"""
        if len(self.enemies) < 3:  # 限制屏幕上同时存在的敌机数量
            enemy = turtle.Turtle()
            enemy.shape("triangle")
            enemy.color("white")
            enemy.shapesize(1, 1)
            enemy.penup()
            enemy.setheading(270)  # 指向屏幕下方
            
            # 随机出现在屏幕顶部
            x = random.randint(-350, 350)
            enemy.goto(x, 280)
            self.enemies.append(enemy)
            
    def move_enemies(self):
        """移动敌机"""
        for enemy in self.enemies[:]:
            enemy.sety(enemy.ycor() - 2)  # 缓慢向下移动
            
            # 检查是否飞出屏幕底部
            if enemy.ycor() < -300:
                enemy.hideturtle()
                self.enemies.remove(enemy)
                
            # 检查与玩家碰撞
            if self.player and self.player.distance(enemy) < 20:
                self.plane_death_animation()
                return
                
    def create_bullet(self):
        """创建子弹"""
        if not self.game_started or self.game_over:
            return
            
        bullet = turtle.Turtle()
        bullet.shape("square")
        bullet.color("cyan")
        bullet.shapesize(0.3, 0.3)
        bullet.penup()
        bullet.goto(self.player.xcor(), self.player.ycor() + 20)
        self.bullets.append(bullet)
        
    def move_bullets(self):
        """移动子弹"""
        for bullet in self.bullets[:]:
            bullet.sety(bullet.ycor() + 10)  # 向上移动
            
            # 检查是否飞出屏幕顶部
            if bullet.ycor() > 300:
                bullet.hideturtle()
                self.bullets.remove(bullet)
                continue
                
            # 检查子弹与敌机碰撞
            for enemy in self.enemies[:]:
                if bullet.distance(enemy) < 20:
                    # 击中敌机
                    bullet.hideturtle()
                    self.bullets.remove(bullet)
                    
                    enemy.hideturtle()
                    self.enemies.remove(enemy)
                    
                    # 增加分数
                    self.manager.add_score(PLANE_ENEMY_POINTS)
                    self.enemies_killed += 1
                    
                    # 显示消息
                    self.show_message()
                    break
                    
    def show_message(self):
        """显示击杀消息 - 红色英文版本"""
        messages = [
            "All the pain you feel stems from that mistake",
            "You're correcting a mistake",
            "Help me",
            "Don't listen to unnecessary voices", 
            "Grant them release, and you will be free, Sergeant",
            "They are monsters"
        ]
        
        if self.enemies_killed <= len(messages):
            message_turtle = turtle.Turtle()
            message_turtle.hideturtle()
            message_turtle.penup()
            message_turtle.color("red")
            message_turtle.goto(0, 250)
            message_turtle.write(messages[self.enemies_killed - 1], 
                               align="center", font=("Arial", 14, "normal"))
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
        return self.enemies_killed >= PLANE_ENEMY_COUNT
        
    def create_particle(self, x, y):
        """创建爆炸粒子 - 类似贪吃蛇死亡特效"""
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
        """飞机死亡动画 - 灰色烟花爆炸，类似贪吃蛇"""
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
        for enemy in self.enemies:
            enemy.hideturtle()
        for bullet in self.bullets:
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
        
        # 设置R键监听器 - 修改为回到标题
        self.screen.listen()
        self.screen.onkeypress(self.restart_to_title, "r")
        self.screen.onkeypress(self.restart_to_title, "R")
        
    def create_blue_spiral_transition(self):
        """创建蓝色螺旋过渡特效"""
        # 创建多个蓝色方块模拟螺旋
        segments = []
        num_segments = 20
        center_x, center_y = 0, 0
        spiral_radius = 10  # 从中心开始
        
        # 创建螺旋段
        for i in range(num_segments):
            segment = turtle.Turtle()
            segment.shape("square")
            segment.color("blue")
            segment.penup()
            segment.goto(center_x, center_y)
            segments.append(segment)
        
        # 螺旋展开动画
        for step in range(30):
            for i, segment in enumerate(segments):
                # 计算螺旋角度
                angle = i * 0.3 + step * 0.1
                # 计算螺旋半径（逐渐扩大）
                radius = spiral_radius + step * 8
                
                # 计算螺旋坐标
                spiral_x = center_x + radius * math.cos(angle)
                spiral_y = center_y + radius * math.sin(angle)
                
                # 移动段到螺旋位置
                segment.goto(spiral_x, spiral_y)
                
                # 段逐渐变成深蓝色
                blue_intensity = max(0.3, 1.0 - i / len(segments))
                segment.color(f"#{int(100 * blue_intensity):02x}{int(100 * blue_intensity):02x}FF")
            
            self.screen.update()
            time.sleep(0.05)
        
        # 蓝色方块充满屏幕
        blue_square = turtle.Turtle()
        blue_square.hideturtle()
        blue_square.penup()
        blue_square.color("blue")
        blue_square.goto(0, 0)
        
        # 蓝色方块从中心扩展到充满屏幕
        for size in range(0, 500, 15):
            blue_square.clear()
            blue_square.dot(size)
            self.screen.update()
            time.sleep(0.02)
        
        # 清除所有元素
        blue_square.hideturtle()
        for segment in segments:
            segment.hideturtle()
            
    def start_game(self):
        """开始游戏"""
        self.game_started = True
        # 清除开始提示
        self.clear_screen()
        self.manager.score_display.update()
        self.create_player()
        
    def restart_to_title(self):
        """返回标题"""
        self.manager.reset_game_score()
        self.manager.change_state(GameState.TITLE)
        
    def transition_to_qte(self):
        """切换到QTE游戏 - 使用回字形特效"""
        # 创建蓝色螺旋过渡特效
        self.create_blue_spiral_transition()
        
        # 显示HERO标题
        self.show_hero_title()
        
    def show_hero_title(self):
        """显示HERO标题 - 使用填充式艺术字"""
        # 清除屏幕
        self.clear_screen()
        
        # 显示填充式HERO艺术字
        hero_turtle = turtle.Turtle()
        hero_turtle.hideturtle()
        hero_turtle.penup()
        hero_turtle.color("white")
        
        # 填充式HERO艺术字（块状风格）
        hero_art = [
            "▓▓▓▓  ▓▓▓▓▓ ▓▓▓▓▓▓▓ ▓▓▓▓▓▓▓  ▓▓▓▓▓▓▓ ",
            "▓▓  ▓▓ ▓▓    ▓▓      ▓▓      ▓▓     ▓▓",
            "▓▓▓▓▓▓ ▓▓▓▓  ▓▓▓▓▓   ▓▓▓▓▓   ▓▓     ▓▓", 
            "▓▓  ▓▓ ▓▓    ▓▓      ▓▓      ▓▓     ▓▓",
            "▓▓  ▓▓ ▓▓▓▓▓ ▓▓▓▓▓▓▓ ▓▓▓▓▓▓▓  ▓▓▓▓▓▓▓ "
        ]
        
        for i, line in enumerate(hero_art):
            hero_turtle.goto(-250, 100 - i * 25)
            hero_turtle.write(line, align="left", font=("Courier", 12, "bold"))
        
        # 副标题
        subtitle = turtle.Turtle()
        subtitle.hideturtle()
        subtitle.penup()
        subtitle.color("white")
        subtitle.goto(0, -80)
        subtitle.write("HERO", align="center", font=("Arial", 20, "bold"))
        
        # 开始提示
        prompt = turtle.Turtle()
        prompt.hideturtle()
        prompt.penup()
        prompt.color("white")
        prompt.goto(0, -150)
        prompt.write("Press SPACE to start", align="center", font=("Arial", 16, "normal"))
        
        self.screen.update()
        
        # 等待玩家按空格开始QTE游戏
        self.screen.listen()
        self.screen.onkeypress(self.start_qte_game, "space")
        
        waiting_for_start = True
        while waiting_for_start and self.manager.current_state == GameState.BLUE_PLANE:
            self.screen.update()
            time.sleep(0.1)
            
    def start_qte_game(self):
        """开始QTE游戏"""
        self.manager.change_state(GameState.BLUE_QTE)
        
    def run(self):
        """运行飞机游戏"""
        self.clear_screen()
        self.manager.score_display.update()
        
        # 第一步：蓝色立方体回字型展开特效
        self.create_blue_spiral()
        
        # 第二步：显示训练场标题
        self.show_training_ground_title()
        
        # 绑定按键
        self.screen.listen()
        self.screen.onkeypress(self.start_game, "space")
        self.screen.onkeypress(self.restart_to_title, "r")
        self.screen.onkeypress(self.restart_to_title, "R")
        
        # 等待玩家按空格开始游戏
        while not self.game_started and self.manager.current_state == GameState.BLUE_PLANE:
            self.screen.update()
            time.sleep(0.1)
            
        # 游戏开始后绑定移动和射击按键
        self.screen.listen()
        self.screen.onkeypress(self.move_left, "Left")
        self.screen.onkeypress(self.move_right, "Right")
        self.screen.onkeypress(self.create_bullet, "space")
        self.screen.onkeypress(self.restart_to_title, "r")
        self.screen.onkeypress(self.restart_to_title, "R")
        
        # 游戏主循环
        enemy_spawn_timer = 0
        while (self.manager.current_state == GameState.BLUE_PLANE and 
               not self.game_over and not self.check_victory()):
            
            # 定期生成敌机
            enemy_spawn_timer += 1
            if enemy_spawn_timer >= 60:  # 每60帧生成一个敌机
                self.create_enemy()
                enemy_spawn_timer = 0
                
            self.move_enemies()
            self.move_bullets()
            
            self.screen.update()
            time.sleep(0.016)  # 约60帧
            
        # 游戏结束或胜利处理
        if self.game_over:
            # 等待玩家按R键
            while self.manager.current_state == GameState.BLUE_PLANE:
                self.screen.update()
                time.sleep(0.1)
        elif self.check_victory():
            # 切换到QTE游戏
            self.transition_to_qte()