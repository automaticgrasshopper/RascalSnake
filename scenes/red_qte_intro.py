import turtle
import time
import math
from scenes.base_scene import BaseScene
from constants import GameState

class RedQTEIntro(BaseScene):
    def __init__(self, game_manager):
        super().__init__(game_manager)
        
    def create_blood_drop_transition(self):
        """创建血滴扩散过渡特效"""
        # 创建血滴中心
        blood_drop = turtle.Turtle()
        blood_drop.hideturtle()
        blood_drop.penup()
        blood_drop.color("dark red")
        blood_drop.goto(0, 0)
        
        # 血滴扩散动画
        for size in range(5, 300, 8):
            blood_drop.clear()
            blood_drop.dot(size, "dark red")
            
            # 添加血滴纹理
            if size > 50:
                for i in range(3):
                    angle = i * 2 * math.pi / 3
                    offset_x = size * 0.3 * math.cos(angle)
                    offset_y = size * 0.3 * math.sin(angle)
                    blood_drop.goto(offset_x, offset_y)
                    blood_drop.dot(size * 0.4, "#8B0000")
            
            self.screen.update()
            time.sleep(0.03)
        
        # 血滴扩散到全屏
        for size in range(300, 800, 15):
            blood_drop.clear()
            blood_drop.dot(size, "#8B0000")
            
            # 添加血色纹理
            if size > 400:
                for i in range(5):
                    angle = i * 2 * math.pi / 5 + time.time() * 0.5
                    offset_x = size * 0.2 * math.cos(angle)
                    offset_y = size * 0.2 * math.sin(angle)
                    blood_drop.goto(offset_x, offset_y)
                    blood_drop.dot(size * 0.3, "#660000")
            
            self.screen.update()
            time.sleep(0.02)
        
        blood_drop.hideturtle()
        
    def fade_red_out(self):
        """红色逐渐褪去，显示内容"""
        # 创建红色覆盖层
        red_overlay = turtle.Turtle()
        red_overlay.hideturtle()
        red_overlay.penup()
        red_overlay.goto(0, 0)
        
        # 红色逐渐变淡直至消失
        for alpha in range(10, -1, -1):
            # 计算当前红色强度
            red_intensity = alpha * 25  # 从250到0
            if red_intensity > 0:
                red_overlay.color(f"#{int(red_intensity):02x}0000")
                red_overlay.dot(1000)  # 足够大的点覆盖整个屏幕
                
            self.screen.update()
            time.sleep(0.08)
        
        red_overlay.hideturtle()
        
    def draw_pistol(self):
        """绘制手枪图形"""
        self.pistol_turtle = turtle.Turtle()
        self.pistol_turtle.hideturtle()
        self.pistol_turtle.speed(0)
        self.pistol_turtle.penup()
        
        # 手枪位置（屏幕中央偏左）
        start_x, start_y = -150, 0
        
        # 绘制手枪主体（白色）
        self.pistol_turtle.color("white")
        self.pistol_turtle.goto(start_x, start_y)
        self.pistol_turtle.pendown()
        self.pistol_turtle.begin_fill()
        
        # 手枪轮廓
        points = [
            (0, 0), (120, 0), (130, -10), (140, -10),
            (150, 0), (160, 10), (160, 30), (150, 40),
            (140, 50), (120, 50), (100, 40), (80, 30),
            (60, 20), (40, 10), (20, 5), (0, 0)
        ]
        
        for x, y in points:
            self.pistol_turtle.goto(start_x + x, start_y + y)
        
        self.pistol_turtle.end_fill()
        self.pistol_turtle.penup()
        
        # 绘制枪管细节（红色）
        self.pistol_turtle.color("red")
        self.pistol_turtle.goto(start_x + 140, start_y + 10)
        self.pistol_turtle.pendown()
        self.pistol_turtle.begin_fill()
        for x, y in [(145, 15), (155, 15), (155, 25), (145, 25)]:
            self.pistol_turtle.goto(start_x + x, start_y + y)
        self.pistol_turtle.end_fill()
        
        # 绘制扳机（红色）
        self.pistol_turtle.penup()
        self.pistol_turtle.goto(start_x + 40, start_y - 5)
        self.pistol_turtle.pendown()
        self.pistol_turtle.begin_fill()
        self.pistol_turtle.circle(8)
        self.pistol_turtle.end_fill()
        
        # 绘制握把纹理（红色条纹）
        self.pistol_turtle.penup()
        for i in range(3):
            y_offset = start_y + 15 + i * 8
            self.pistol_turtle.goto(start_x + 60, y_offset)
            self.pistol_turtle.pendown()
            self.pistol_turtle.goto(start_x + 90, y_offset)
            self.pistol_turtle.penup()
        
        self.pistol_turtle.hideturtle()
        
    def show_killer_title(self):
        """显示KILLER艺术字"""
        self.title_turtle = turtle.Turtle()
        self.title_turtle.hideturtle()
        self.title_turtle.penup()
        self.title_turtle.color("red")
        
        # KILLER 艺术字（精简版）
        title_art = [
            "╦╔═╗╦╔═╔═╗╔═╗╦ ╦",
            "║╠═╝╠╩╗║╣ ║  ╠═╣", 
            "╩╩  ╩ ╩╚═╝╚═╝╩ ╩"
        ]
        
        # 艺术字放在右侧
        start_x, start_y = 100, 50
        
        for i, line in enumerate(title_art):
            self.title_turtle.goto(start_x, start_y - i * 30)
            self.title_turtle.write(line, align="left", font=("Courier", 16, "bold"))
        
    def show_subtitle(self):
        """显示副标题和开始提示"""
        # 副标题
        self.subtitle_turtle = turtle.Turtle()
        self.subtitle_turtle.hideturtle()
        self.subtitle_turtle.penup()
        self.subtitle_turtle.color("white")
        self.subtitle_turtle.goto(0, -150)
        self.subtitle_turtle.write("KILLER", align="center", font=("Arial", 20, "bold"))
        
        # 开始提示
        self.prompt_turtle = turtle.Turtle()
        self.prompt_turtle.hideturtle()
        self.prompt_turtle.penup()
        self.prompt_turtle.color("yellow")
        self.prompt_turtle.goto(0, -200)
        self.prompt_turtle.write("Press SPACE to continue", align="center", font=("Arial", 14, "normal"))
        
    def start_game(self):
        """开始游戏"""
        self.manager.change_state(GameState.RED_QTE)
        
    def run(self):
        """运行红色QTE介绍场景"""
        self.clear_screen()
        
        # 第一步：血滴扩散过渡特效
        self.create_blood_drop_transition()
        
        # 第二步：红色逐渐褪去
        self.fade_red_out()
        
        # 第三步：直接显示所有内容
        self.draw_pistol()
        self.show_killer_title()
        self.show_subtitle()
        self.screen.update()
        
        # 绑定按键
        self.screen.listen()
        self.screen.onkeypress(self.start_game, "space")
        
        # 等待开始
        while self.manager.current_state == GameState.RED_QTE_INTRO:
            self.screen.update()
            time.sleep(0.05)