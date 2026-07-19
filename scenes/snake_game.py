import turtle
import time
import random
import math
from scenes.base_scene import BaseScene
from constants import GameState, WALL_COLOR, SNAKE_HEAD_COLOR, SNAKE_BODY_COLORS
from constants import FOOD_COLOR, FOOD_POINTS, PURPLE_ENDING_SCORE, SPECIAL_FOOD_SPAWN_SCORE, SNAKE_SPEED

class SnakeGame(BaseScene):
    def __init__(self, game_manager):
        super().__init__(game_manager)
        self.reset_game_state()
        
    def reset_game_state(self):
        """完全重置游戏状态"""
        self.snake = []
        self.food = None
        self.special_foods = []
        self.walls = []
        self.direction = "Right"
        self.next_direction = "Right"
        self.is_dead = False
        self.death_animation_complete = False
        self.particles = []  # 用于死亡动画的粒子
        self.special_foods_spawned = False  # 标记特殊食物是否已生成
        
    def create_walls(self):
        """创建灰色围墙"""
        # 上下围墙
        for x in range(-380, 381, 20):
            # 上围墙
            wall_top = self.create_wall_segment(x, 280)
            # 下围墙  
            wall_bottom = self.create_wall_segment(x, -300)
            self.walls.extend([wall_top, wall_bottom])
            
        # 左右围墙
        for y in range(-280, 301, 20):
            # 左围墙
            wall_left = self.create_wall_segment(-400, y)
            # 右围墙
            wall_right = self.create_wall_segment(380, y)
            self.walls.extend([wall_left, wall_right])
            
    def create_wall_segment(self, x, y):
        """创建单个围墙段"""
        wall = turtle.Turtle()
        wall.shape("square")
        wall.color(WALL_COLOR)
        wall.penup()
        wall.goto(x, y)
        # 添加一些纹理变化，使围墙不那么单调
        if random.random() > 0.7:
            wall.color("#909090")  # 稍亮一点的灰色
        elif random.random() < 0.2:
            wall.color("#707070")  # 稍暗一点的灰色
        return wall
        
    def create_snake(self):
        """创建带有渐变紫色的蛇，固定在中心位置"""
        # 固定起始位置在中心 (0, 0)
        start_x, start_y = 0, 0
        
        for i in range(3):
            segment = turtle.Turtle()
            segment.shape("square")
            # 根据位置设置渐变颜色
            color_index = min(i, len(SNAKE_BODY_COLORS) - 1)
            if i == 0:  # 蛇头
                segment.color(SNAKE_HEAD_COLOR)
            else:  # 蛇身使用渐变
                segment.color(SNAKE_BODY_COLORS[color_index])
            segment.penup()
            
            # 设置蛇段位置，固定在中心
            segment_x = start_x - i * 20
            segment_y = start_y
            
            segment.goto(segment_x, segment_y)
            
            # 添加赖皮效果 - 轻微随机偏移
            segment.goto(segment_x + random.randint(-1, 1), 
                        segment_y + random.randint(-1, 1))
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
                
    def create_food(self):
        """创建食物，带有赖皮效果"""
        self.food = turtle.Turtle()
        self.food.shape("circle")
        self.food.color(FOOD_COLOR)
        self.food.penup()
        self.move_food()
        
    def move_food(self):
        """移动食物到随机位置，避开围墙"""
        while True:
            x = (random.randint(-17, 17) * 20)
            y = (random.randint(-12, 12) * 20)
            # 检查是否在围墙内
            if (-360 <= x <= 360 and -260 <= y <= 260):
                self.food.goto(x, y)
                # 赖皮效果：食物轻微跳动
                self.food.goto(x + random.randint(-2, 2), 
                              y + random.randint(-2, 2))
                break
                
    def create_special_foods(self):
        """创建特殊食物（红色和蓝色）"""
        if not self.special_foods:
            blue_food = turtle.Turtle()
            blue_food.shape("circle")
            blue_food.color("blue")
            blue_food.penup()
            
            red_food = turtle.Turtle()
            red_food.shape("circle")
            red_food.color("red")
            red_food.penup()
            
            # 放置特殊食物，确保在安全区域内
            blue_food.goto(-100, 100)
            red_food.goto(100, 100)
            
            # 赖皮效果：特殊食物也会动
            blue_food.goto(-100 + random.randint(-5, 5), 
                          100 + random.randint(-5, 5))
            red_food.goto(100 + random.randint(-5, 5), 
                         100 + random.randint(-5, 5))
            
            self.special_foods = [blue_food, red_food]
            self.special_foods_spawned = True
            
    def remove_special_foods(self):
        """移除特殊食物"""
        for food in self.special_foods:
            food.hideturtle()
        self.special_foods.clear()
        
    def check_collision(self):
        """检查碰撞，包括围墙和自身"""
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
        head = self.snake[0]
        
        # 检查普通食物碰撞
        if head.distance(self.food) < 20:
            self.manager.add_score(FOOD_POINTS)  # 每次吃食物固定加37分
            self.move_food()
            self.add_segment()
            
            # 如果吃了紫色食物且特殊食物已生成，则移除特殊食物
            if self.special_foods:
                self.remove_special_foods()
                
            return "normal"
            
        # 检查特殊食物碰撞
        for i, food in enumerate(self.special_foods):
            if head.distance(food) < 20:
                food_type = "blue" if i == 0 else "red"
                self.remove_special_foods()
                return food_type
                
        return None
        
    def add_segment(self):
        """添加蛇身段，使用渐变颜色"""
        segment = turtle.Turtle()
        segment.shape("square")
        # 根据蛇长度选择颜色
        color_index = min(len(self.snake) - 1, len(SNAKE_BODY_COLORS) - 1)
        segment.color(SNAKE_BODY_COLORS[color_index])
        segment.penup()
        # 放在最后一个段的位置
        last_segment = self.snake[-1]
        segment.goto(last_segment.xcor(), last_segment.ycor())
        self.snake.append(segment)
        
    def move(self):
        """移动蛇，应用赖皮效果"""
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
        restart_text.write("Press R to Restart", align="center", font=("Arial", 16, "normal"))
        
        self.screen.update()
        self.death_animation_complete = True
        
        # 设置R键监听器
        self.screen.listen()
        self.screen.onkeypress(self.restart_game, "r")
        self.screen.onkeypress(self.restart_game, "R")
        
    def restart_game(self):
        """重新开始游戏"""
        if self.is_dead:
            # 清除所有粒子
            for particle, _, _ in self.particles:
                particle.hideturtle()
            self.particles.clear()
            
            # 重置游戏状态
            self.manager.restart_to_title()
            
    def game_over(self):
        """游戏结束处理"""
        # 播放死亡动画
        self.death_animation()
        
        # 等待玩家按R键
        while self.is_dead and self.manager.current_state == GameState.SNAKE_GAME:
            self.screen.update()
            time.sleep(0.1)
            
    def transition_to_purple_ending(self):
        """新的紫色结局转场动画 - 蛇蜷缩成回字立方体"""
        # 清除所有按键绑定
        self.screen.listen()
        self.screen.onkeypress(None, "Up")
        self.screen.onkeypress(None, "Down")
        self.screen.onkeypress(None, "Left")
        self.screen.onkeypress(None, "Right")
        
        # 第一步：蛇蜷缩成回字形
        center_x, center_y = 0, 0
        spiral_radius = 100  # 初始螺旋半径
        
        # 计算蛇头到中心的距离
        head = self.snake[0]
        head_x, head_y = head.position()
        
        # 将蛇移动到中心附近开始蜷缩
        for segment in self.snake:
            seg_x, seg_y = segment.position()
            segment.goto(seg_x - head_x, seg_y - head_y)
        
        # 蜷缩动画 - 蛇身逐渐形成螺旋形
        for step in range(30):
            for i, segment in enumerate(self.snake):
                # 计算螺旋角度
                angle = i * 0.3 + step * 0.1
                # 计算螺旋半径（逐渐缩小）
                radius = spiral_radius * (1 - step / 40)
                
                # 计算螺旋坐标
                spiral_x = center_x + radius * math.cos(angle)
                spiral_y = center_y + radius * math.sin(angle)
                
                # 移动蛇段到螺旋位置
                segment.goto(spiral_x, spiral_y)
                
                # 蛇段逐渐变成深紫色
                purple_intensity = max(0.3, 1.0 - i / len(self.snake))
                segment.color(f"#{int(100 * purple_intensity):02x}00{int(200 * purple_intensity):02x}")
            
            self.screen.update()
            time.sleep(0.05)
        
        # 第二步：形成立方体
        cube_size = 40
        for step in range(20):
            for i, segment in enumerate(self.snake):
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
                
                # 所有蛇段变成深紫色
                segment.color("#6A0DAD")
                
            self.screen.update()
            time.sleep(0.05)
        
        # 第三步：紫色蔓延浸染屏幕
        purple_overlay = turtle.Turtle()
        purple_overlay.hideturtle()
        purple_overlay.penup()
        purple_overlay.goto(0, 0)
        purple_overlay.color("#6A0DAD")
        
        # 从立方体中心开始，紫色逐渐扩散
        for radius in range(0, 500, 10):
            purple_overlay.clear()
            purple_overlay.dot(radius * 2)
            self.screen.update()
            time.sleep(0.02)
        
        # 第四步：紫色像油漆一样褪下，露出墓碑
        for radius in range(500, 0, -15):
            # 清除紫色覆盖层
            purple_overlay.clear()
            
            # 绘制逐渐缩小的紫色圆
            if radius > 0:
                purple_overlay.dot(radius * 2)
            
            self.screen.update()
            time.sleep(0.02)
        
        # 隐藏紫色覆盖层
        purple_overlay.hideturtle()
        
        # 保存游戏状态并切换到紫色结局
        self.manager.save_data.purple_completed = True
        from save_manager import SaveManager
        SaveManager.save_game(self.manager.save_data)
        
        # 短暂暂停后切换到紫色结局场景
        time.sleep(1)
        self.manager.change_state(GameState.PURPLE_ENDING)
        
    def transition_to_blue(self):
        """进入蓝色模式的转场"""
        for segment in self.snake:
            segment.shape("square")
            segment.shapesize(2, 2)
            segment.color("blue")
            
        self.screen.update()
        time.sleep(1)
        
        # 切换到蓝色模式
        self.manager.change_state(GameState.BLUE_MODE)
        
    def transition_to_red(self):
        """进入红色模式的转场"""
        # 清除蛇身
        for segment in self.snake:
            segment.hideturtle()
        
        # 隐藏食物
        if self.food:
            self.food.hideturtle()
        
        # 隐藏特殊食物
        for food in self.special_foods:
            food.hideturtle()
        
        # 显示红色转场效果
        red_overlay = turtle.Turtle()
        red_overlay.hideturtle()
        red_overlay.penup()
        red_overlay.goto(0, 0)
        red_overlay.color("red")
        
        # 红色逐渐充满屏幕
        for radius in range(0, 500, 15):
            red_overlay.clear()
            red_overlay.dot(radius * 2)
            self.screen.update()
            time.sleep(0.02)
        
        # 短暂显示红色屏幕
        time.sleep(0.5)
        
        # 红色逐渐褪去
        for radius in range(500, 0, -20):
            red_overlay.clear()
            if radius > 0:
                red_overlay.dot(radius * 2)
            self.screen.update()
            time.sleep(0.02)
        
        red_overlay.hideturtle()
        
        # 切换到红色六芒星验证场景
        self.manager.change_state(GameState.RED_STAR_VERIFICATION)
        
    def run(self):
        # 每次运行游戏时完全重置状态
        self.reset_game_state()
        
        self.clear_screen()
        self.manager.score_display.update()
        
        # 初始化游戏元素
        self.create_walls()
        self.create_snake()
        self.create_food()
        
        # 绑定按键
        self.screen.listen()
        self.screen.onkeypress(self.go_up, "Up")
        self.screen.onkeypress(self.go_down, "Down")
        self.screen.onkeypress(self.go_left, "Left")
        self.screen.onkeypress(self.go_right, "Right")
        
        while self.manager.current_state == GameState.SNAKE_GAME and not self.is_dead:
            self.move()
            
            if self.check_collision():
                self.game_over()
                break
                
            food_result = self.check_food_collision()
            if food_result == "normal":
                # 检查是否需要生成特殊食物（只在666分且未生成过时）
                if (self.manager.current_game_score == SPECIAL_FOOD_SPAWN_SCORE and 
                    not self.special_foods_spawned):
                    self.create_special_foods()
                    
            elif food_result == "blue":
                self.transition_to_blue()
                break
            elif food_result == "red":
                self.transition_to_red()
                break
                
            if self.manager.current_game_score >= PURPLE_ENDING_SCORE:
                self.transition_to_purple_ending()
                break
                
            # 更新分数显示（确保666分时变红）
            self.manager.score_display.update()
            self.screen.update()
            time.sleep(SNAKE_SPEED)