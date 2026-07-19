import turtle
import time
import math
import random
from scenes.base_scene import BaseScene
from constants import GameState
from save_manager import SaveManager

class RedEnding(BaseScene):
    def __init__(self, game_manager):
        super().__init__(game_manager)
        self.current_stage = "tombstones"  # tombstones, computer, cerberus
        self.input_code = ""
        self.waiting_for_space = False
        self.tombstones_displayed = False
        self.computer_displayed = False
        self.cerberus_displayed = False
        
    def show_three_tombstones(self):
        """显示三个墓碑"""
        self.clear_screen()
        
        # 墓碑数据
        tombstones_data = [
            {"name": "MIKE CODE", "years": "1999-2025"},
            {"name": "ALEX CODE", "years": "1999-2025"}, 
            {"name": "TODD CODE", "years": "1999-2025"}
        ]
        
        positions = [(-200, 0), (0, 0), (200, 0)]
        
        # 绘制三个墓碑
        for i, (pos, data) in enumerate(zip(positions, tombstones_data)):
            self.draw_tombstone(pos[0], pos[1], data["name"], data["years"])
            
        # 底部文字
        epitaph = turtle.Turtle()
        epitaph.hideturtle()
        epitaph.penup()
        epitaph.color("red")
        epitaph.goto(0, -150)
        epitaph.write("He killed them, and at last himself", 
                     align="center", font=("Arial", 14, "normal"))
        
        # 继续提示
        continue_prompt = turtle.Turtle()
        continue_prompt.hideturtle()
        continue_prompt.penup()
        continue_prompt.color("yellow")
        continue_prompt.goto(0, -200)
        continue_prompt.write("Press SPACE to continue", align="center", 
                             font=("Arial", 16, "normal"))
        
        self.tombstones_displayed = True
        self.current_stage = "tombstones"
        self.screen.update()
        
    def draw_tombstone(self, x, y, name, years):
        """绘制单个墓碑"""
        tombstone = turtle.Turtle()
        tombstone.hideturtle()
        tombstone.penup()
        tombstone.color("red")
        
        # 墓碑形状
        tombstone_art = [
            "  _____________",
            " |             |",
            " |   REST IN   |", 
            " |    PEACE    |",
            " |             |",
            f" |  {name}  |",
            f" |  {years}  |",
            " |_____________|",
            "      |   |",
            "      |   |",
            "     _|___|_"
        ]
        
        for i, line in enumerate(tombstone_art):
            tombstone.goto(x - 90, y + 100 - i * 20)
            tombstone.write(line, align="left", font=("Courier", 10, "normal"))
            
    def show_computer_screen(self):
        """显示电脑屏幕"""
        self.clear_screen()
        
        # 电脑显示器 - 红色
        computer = turtle.Turtle()
        computer.hideturtle()
        computer.penup()
        computer.color("red")
        
        # 显示器框架 - 红色
        computer_frame = [
            "     ____________________________",
            "    !\\_________________________/!\\",
            "    !!                         !! \\",
            "    !!                         !!  \\", 
            "    !!                         !!  !",
            "    !!                         !!  !",
            "    !!     KILLER VICTORY!     !!  !",
            "    !!                         !!  !",
            "    !!                         !!  !",
            "    !!                         !!  /",
            "    !!_________________________!! /",
            "    !/_________________________\\!/",
            "       __\\_________________/__/!_",
            "      !_______________________!/",
            "    ________________________",
            "   /oooo  oooo  oooo  oooo /!",
            "  /ooooooooooooooooooooooo/ /",
            " /ooooooooooooooooooooooo/ /",
            "/CODE=MIKE______________/_/"
        ]
        
        for i, line in enumerate(computer_frame):
            computer.goto(-350, 200 - i * 20)
            computer.write(line, align="left", font=("Courier", 8, "normal"))
            
        # CODE 字样 - 红色
        code_text = turtle.Turtle()
        code_text.hideturtle()
        code_text.penup()
        code_text.color("red")
        code_text.goto(-50, -50)
        code_text.write("CODE", align="center", font=("Arial", 16, "bold"))
        
        # 输入提示 - 红色
        input_prompt = turtle.Turtle()
        input_prompt.hideturtle()
        input_prompt.penup()
        input_prompt.color("red")
        input_prompt.goto(-100, -100)
        input_prompt.write("Enter the final CODE: ", align="left", font=("Arial", 12, "normal"))
        
        self.computer_displayed = True
        self.current_stage = "computer"
        self.screen.update()
        
    def draw_cerberus(self):
        """绘制地狱三头犬 - 蛇头狗身"""
        cerberus = turtle.Turtle()
        cerberus.hideturtle()
        cerberus.penup()
        cerberus.color("red")
        cerberus.width(3)
        
        # 身体位置
        body_x, body_y = 0, 0
        
        # 绘制狗的身体
        cerberus.goto(body_x, body_y)
        cerberus.pendown()
        
        # 身体轮廓
        body_points = [
            (-80, -100), (-120, -60), (-120, 0), (-80, 40),
            (80, 40), (120, 0), (120, -60), (80, -100), (-80, -100)
        ]
        
        for point in body_points:
            cerberus.goto(body_x + point[0], body_y + point[1])
        
        cerberus.penup()
        
        # 绘制三个蛇头
        head_positions = [(-120, 40), (0, 80), (120, 40)]  # 左、中、右头的位置
        
        for i, (head_x, head_y) in enumerate(head_positions):
            self.draw_snake_head(cerberus, body_x + head_x, body_y + head_y, i)
        
        cerberus.hideturtle()
        
    def draw_snake_head(self, turtle_obj, x, y, head_type):
        """绘制蛇头"""
        turtle_obj.penup()
        turtle_obj.goto(x, y)
        turtle_obj.pendown()
        
        # 根据头部类型调整形状
        if head_type == 0:  # 左头
            # 蛇头形状 - 向左
            points = [
                (0, 0), (-40, 20), (-60, 0), (-40, -20), (0, 0)
            ]
        elif head_type == 1:  # 中头
            # 蛇头形状 - 向上
            points = [
                (0, 0), (-20, 40), (0, 60), (20, 40), (0, 0)
            ]
        else:  # 右头
            # 蛇头形状 - 向右
            points = [
                (0, 0), (40, 20), (60, 0), (40, -20), (0, 0)
            ]
        
        for point in points:
            turtle_obj.goto(x + point[0], y + point[1])
        
        # 绘制眼睛 - 红色发光的眼睛
        turtle_obj.penup()
        if head_type == 0:  # 左头眼睛
            turtle_obj.goto(x - 30, y + 10)
        elif head_type == 1:  # 中头眼睛
            turtle_obj.goto(x - 10, y + 30)
        else:  # 右头眼睛
            turtle_obj.goto(x + 30, y + 10)
        
        turtle_obj.dot(8, "red")
        
        # 绘制蛇信子
        turtle_obj.penup()
        if head_type == 0:  # 左头信子
            turtle_obj.goto(x - 60, y)
            turtle_obj.pendown()
            turtle_obj.goto(x - 75, y - 5)
            turtle_obj.penup()
            turtle_obj.goto(x - 60, y)
            turtle_obj.pendown()
            turtle_obj.goto(x - 75, y + 5)
        elif head_type == 1:  # 中头信子
            turtle_obj.goto(x, y + 60)
            turtle_obj.pendown()
            turtle_obj.goto(x - 5, y + 75)
            turtle_obj.penup()
            turtle_obj.goto(x, y + 60)
            turtle_obj.pendown()
            turtle_obj.goto(x + 5, y + 75)
        else:  # 右头信子
            turtle_obj.goto(x + 60, y)
            turtle_obj.pendown()
            turtle_obj.goto(x + 75, y - 5)
            turtle_obj.penup()
            turtle_obj.goto(x + 60, y)
            turtle_obj.pendown()
            turtle_obj.goto(x + 75, y + 5)
        
        turtle_obj.penup()
        
    def show_cerberus(self):
        """显示地狱三头犬 - 修改：不立即清屏"""
        # 只在第一次显示时清屏
        if not self.cerberus_displayed:
            self.clear_screen()
        
        # 绘制地狱三头犬
        self.draw_cerberus()
        
        # 绘制召唤特效
        self.draw_summoning_effect()
        
        # 感谢文字 - 带血迹效果
        self.draw_thanks_message()
        
        # 退出提示
        exit_prompt = turtle.Turtle()
        exit_prompt.hideturtle()
        exit_prompt.penup()
        exit_prompt.color("yellow")
        exit_prompt.goto(0, -250)
        exit_prompt.write("SPACE TO EXIT", 
                         align="center", font=("Arial", 14, "normal"))
        
        self.cerberus_displayed = True
        self.current_stage = "cerberus"
        self.waiting_for_space = True
        self.screen.update()
        
    def draw_summoning_effect(self):
        """绘制召唤特效"""
        effect = turtle.Turtle()
        effect.hideturtle()
        effect.penup()
        effect.color("red")
        effect.width(2)
        
        # 绘制魔法阵
        effect.goto(0, -150)
        effect.pendown()
        
        # 外圆
        effect.circle(200)
        
        # 内圆
        effect.penup()
        effect.goto(0, -100)
        effect.pendown()
        effect.circle(150)
        
        # 六芒星
        effect.penup()
        effect.goto(0, -50)
        effect.pendown()
        
        for i in range(6):
            effect.forward(100)
            effect.backward(100)
            effect.left(60)
        
        effect.penup()
        
        # 绘制能量粒子
        for _ in range(20):
            x = random.randint(-180, 180)
            y = random.randint(-180, 180)
            effect.goto(x, y)
            effect.dot(5, "red")
        
    def draw_thanks_message(self):
        """绘制感谢文字 - 带血迹效果"""
        thanks = turtle.Turtle()
        thanks.hideturtle()
        thanks.penup()
        thanks.color("red")
        thanks.goto(0, -200)
        
        # 主要文字
        thanks.write("Thanks for your SUMMONING (=^_^=)", 
                    align="center", font=("Arial", 16, "bold"))
        
        # 血迹效果
        blood = turtle.Turtle()
        blood.hideturtle()
        blood.penup()
        blood.color("darkred")
        
        # 在文字周围添加血迹滴落效果
        blood_positions = [
            (-120, -190), (-100, -210), (-80, -195),
            (80, -190), (100, -210), (120, -195),
            (-20, -220), (20, -220), (0, -230)
        ]
        
        for pos in blood_positions:
            blood.goto(pos[0], pos[1])
            blood.dot(random.randint(3, 8))
            
        # 添加血迹流动效果
        blood.width(2)
        for i in range(3):
            start_x = random.randint(-150, 150)
            start_y = -185
            blood.goto(start_x, start_y)
            blood.pendown()
            for j in range(5):
                blood.goto(start_x + random.randint(-10, 10), 
                          start_y - j * 8 - random.randint(0, 5))
            blood.penup()
        
    def setup_input(self):
        """设置输入框"""
        self.input_code = ""
        self.show_input_display()
        
    def show_input_display(self):
        """显示输入框"""
        # 清除之前的输入显示
        for turtle_obj in self.screen.turtles():
            if hasattr(turtle_obj, 'is_input_display'):
                turtle_obj.clear()
                
        # 显示当前输入
        input_display = turtle.Turtle()
        input_display.hideturtle()
        input_display.penup()
        input_display.is_input_display = True
        input_display.color("red")  # 改为红色
        input_display.goto(50, -100)
        display_text = self.input_code if self.input_code else "____"
        input_display.write(display_text, align="left", font=("Courier", 16, "bold"))
        
    def process_keypress(self, key):
        """处理按键"""
        if self.current_stage != "computer":
            return
            
        if key == "BackSpace":
            if self.input_code:
                self.input_code = self.input_code[:-1]
        elif key.isalpha() and len(key) == 1:
            if len(self.input_code) < 4:
                self.input_code += key.upper()
        elif key == "Return":
            self.check_code()
                
        self.show_input_display()
        
    def check_code(self):
        """检查代码"""
        if self.input_code.upper() == "MIKE":
            self.code_correct()
        else:
            self.code_incorrect()
            
    def code_correct(self):
        """代码正确"""
        correct = turtle.Turtle()
        correct.hideturtle()
        correct.penup()
        correct.color("#00FF00")
        correct.goto(0, -150)
        correct.write("✓ CODE ACCEPTED ✓", align="center", font=("Arial", 16, "bold"))
        
        self.screen.update()
        time.sleep(1.5)  # 缩短等待时间
        
        # 显示地狱三头犬
        self.transition_to_cerberus()
        
    def code_incorrect(self):
        """代码错误"""
        error = turtle.Turtle()
        error.hideturtle()
        error.penup()
        error.color("#FF0000")
        error.goto(0, -150)
        error.write("✗ INCORRECT CODE ✗", align="center", font=("Arial", 16, "bold"))
        
        self.input_code = ""
        self.show_input_display()
        
        self.screen.update()
        time.sleep(1.5)
        error.clear()
        
    def transition_to_computer(self):
        """过渡到电脑屏幕 - 改进的绘图特效"""
        if self.current_stage == "tombstones":
            # 创建绘图特效 - 从墓碑逐渐变形为显示器
            self.draw_transition_effect()
            
            # 显示电脑屏幕
            self.show_computer_screen()
            
            # 设置输入
            self.setup_input()
            
    def draw_transition_effect(self):
        """绘制过渡特效 - 从墓碑到显示器的变形过程"""
        transition = turtle.Turtle()
        transition.hideturtle()
        transition.penup()
        transition.color("red")
        
        # 第一阶段：墓碑逐渐溶解
        for step in range(10):
            self.clear_screen()
            transition.goto(0, 0)
            
            # 绘制逐渐模糊的墓碑
            for i in range(3):
                x = [-200, 0, 200][i]
                y = 0
                
                # 墓碑逐渐变形
                distortion = step * 5
                transition.goto(x - 90 + random.randint(-distortion, distortion), 
                               y + 100 + random.randint(-distortion, distortion))
                
                tombstone_art = [
                    "  _____________",
                    " |             |",
                    " |   REST IN   |", 
                    " |    PEACE    |",
                    " |             |",
                    " |  CODE       |",
                    " |             |",
                    " |_____________|",
                ]
                
                for j, line in enumerate(tombstone_art):
                    transition.goto(x - 90 + random.randint(-distortion, distortion), 
                                   y + 100 - j * 20 + random.randint(-distortion, distortion))
                    transition.write(line, align="left", font=("Courier", 10, "normal"))
            
            self.screen.update()
            time.sleep(0.1)
        
        # 第二阶段：红色像素化过渡
        pixels = []
        for _ in range(50):
            pixel = turtle.Turtle()
            pixel.shape("square")
            pixel.color("red")
            pixel.shapesize(0.5)
            pixel.penup()
            pixel.goto(random.randint(-400, 400), random.randint(-300, 300))
            pixels.append(pixel)
        
        for size in range(1, 3):
            for pixel in pixels:
                pixel.shapesize(size)
            self.screen.update()
            time.sleep(0.05)
        
        # 第三阶段：像素汇聚成显示器轮廓
        for pixel in pixels:
            pixel.hideturtle()
        
        # 绘制显示器轮廓逐渐形成
        computer_outline = turtle.Turtle()
        computer_outline.hideturtle()
        computer_outline.penup()
        computer_outline.color("red")
        computer_outline.width(2)
        
        # 显示器轮廓点
        frame_points = [
            (-300, 200), (300, 200), (300, -100), (-300, -100), (-300, 200)
        ]
        
        # 逐渐绘制轮廓
        computer_outline.goto(frame_points[0])
        computer_outline.pendown()
        
        for point in frame_points[1:]:
            for step in range(10):
                current_pos = computer_outline.position()
                target_x = current_pos[0] + (point[0] - current_pos[0]) * 0.1
                target_y = current_pos[1] + (point[1] - current_pos[1]) * 0.1
                computer_outline.goto(target_x, target_y)
                self.screen.update()
                time.sleep(0.02)
        
        computer_outline.penup()
        time.sleep(0.5)
            
    def transition_to_cerberus(self):
        """过渡到地狱三头犬 - 使用更炫酷的魔法阵效果"""
        # 清除电脑屏幕
        self.clear_screen()
        
        # 创建炫酷的魔法阵
        self.draw_cool_magic_circle()
        
        # 快速粒子汇聚效果
        self.draw_quick_particle_effect()
        
        # 短暂延迟后显示地狱三头犬
        time.sleep(0.5)
        
        # 显示地狱三头犬
        self.show_cerberus()
        
    def draw_cool_magic_circle(self):
        """绘制炫酷的魔法阵"""
        # 创建多个海龟对象用于绘制不同部分
        circle_turtle = turtle.Turtle()
        circle_turtle.hideturtle()
        circle_turtle.speed(0)
        circle_turtle.penup()
        
        star_turtle = turtle.Turtle()
        star_turtle.hideturtle()
        star_turtle.speed(0)
        star_turtle.penup()
        
        # 绘制彩色螺旋星形
        for i in range(100):
            r = random.random()
            g = random.random()
            b = random.random()
            star_turtle.pencolor(r, g, b)
            star_turtle.forward(i * 2)
            star_turtle.right(144)
            self.screen.update()
            time.sleep(0.01)
        
        # 绘制多层魔法阵
        colors = ["red", "darkred", "orange", "yellow"]
        for i, color in enumerate(colors):
            circle_turtle.pencolor(color)
            circle_turtle.width(3 - i * 0.5)
            circle_turtle.goto(0, -50 * (i + 1))
            circle_turtle.pendown()
            circle_turtle.circle(50 * (i + 1))
            circle_turtle.penup()
            self.screen.update()
            time.sleep(0.1)
        
        # 绘制符文
        runes = ["Ψ", "Φ", "Σ", "Ω", "Δ", "Θ"]
        rune_turtle = turtle.Turtle()
        rune_turtle.hideturtle()
        rune_turtle.penup()
        rune_turtle.color("red")
        
        for i, rune in enumerate(runes):
            angle = i * (360 / len(runes))
            rad = math.radians(angle)
            x = math.cos(rad) * 150
            y = math.sin(rad) * 150
            rune_turtle.goto(x, y)
            rune_turtle.write(rune, align="center", font=("Arial", 20, "bold"))
        
        self.screen.update()
        
    def draw_quick_particle_effect(self):
        """快速粒子效果"""
        particles = []
        
        # 创建粒子
        for _ in range(40):
            particle = turtle.Turtle()
            particle.shape("circle")
            particle.color("red")
            particle.shapesize(0.3)
            particle.penup()
            
            # 从屏幕边缘飞向中心
            angle = random.uniform(0, 2 * math.pi)
            distance = 400
            start_x = math.cos(angle) * distance
            start_y = math.sin(angle) * distance
            particle.goto(start_x, start_y)
            particles.append(particle)
        
        # 快速飞向中心
        for step in range(15):  # 减少步骤数
            for particle in particles:
                current_x, current_y = particle.position()
                target_x = current_x * 0.8
                target_y = current_y * 0.8
                particle.goto(target_x, target_y)
            
            self.screen.update()
            time.sleep(0.03)  # 减少延迟
        
        # 快速爆炸效果
        for step in range(8):  # 减少步骤数
            for particle in particles:
                current_x, current_y = particle.position()
                # 向外扩散
                explosion_x = current_x * (1 + step * 0.3)
                explosion_y = current_y * (1 + step * 0.3)
                particle.goto(explosion_x, explosion_y)
                # 逐渐变大
                particle.shapesize(0.3 + step * 0.2)
            
            self.screen.update()
            time.sleep(0.03)  # 减少延迟
        
        # 隐藏所有粒子
        for particle in particles:
            particle.hideturtle()
        
    def handle_space_press(self):
        """处理空格键按下"""
        if self.current_stage == "tombstones":
            self.transition_to_computer()
        elif self.current_stage == "cerberus":
            self.exit_game()
            
    def exit_game(self):
        """退出游戏并保存状态"""
        # 保存游戏状态
        self.manager.save_data.red_form_completed = True
        # 更新历史总分
        if self.manager.session_total_score > self.manager.save_data.historical_total:
            self.manager.save_data.historical_total = self.manager.session_total_score
        SaveManager.save_game(self.manager.save_data)
        
        # 退出游戏
        self.manager.screen.bye()
        
    def run(self):
        """运行红色墓碑场景"""
        # 第一阶段：显示三个墓碑
        self.show_three_tombstones()
        
        # 绑定按键
        self.screen.listen()
        self.screen.onkeypress(self.handle_space_press, "space")
        
        # 绑定输入按键（用于电脑屏幕阶段）
        for char in "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz":
            self.screen.onkeypress(lambda ch=char: self.process_keypress(ch), char)
        self.screen.onkeypress(lambda: self.process_keypress("BackSpace"), "BackSpace")
        self.screen.onkeypress(lambda: self.process_keypress("Return"), "Return")
        
        # 主循环
        while self.manager.current_state == GameState.RED_ENDING:
            self.screen.update()
            time.sleep(0.1)