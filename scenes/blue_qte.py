import turtle
import time
import random
import math
from scenes.base_scene import BaseScene
from constants import GameState
from save_manager import SaveManager

class BlueQTE(BaseScene):
    def __init__(self, game_manager):
        super().__init__(game_manager)
        
        # 游戏状态
        self.score = 0
        self.game_over = False
        self.current_mode = "hero_intro"  # 直接开始游戏，跳过标题
        self.transition_timer = 120
        self.game_started = True  # 标记游戏已开始
        self.hero_progress = 0
        self.sequence_step = 0
        self.current_sequence = []
        self.sequence_complete = False
        self.monster_health = 15
        self.current_timer = 0
        self.max_timer = 90
        self.combo_count = 0
        self.perfect_count = 0
        self.total_sequences = 3
        self.current_round = 1
        
        # 初始化系统
        self.hero_system = HeroSystem()
        self.firework_system = FireworkSystem()
        self.tombstone_system = TombstoneSystem()
        self.display_system = DisplaySystem()
        
    def start_game(self):
        """开始游戏"""
        self.current_mode = "hero_intro"
        self.transition_timer = 120
        self.hero_system.show_hero()
        self.hero_system.show_monster()
        self.display_system.update_state("DEFEAT THE MONSTER IN 3 ROUNDS OF QTE!")
        
    def start_hero_sequence(self):
        self.current_mode = "hero_sequence"
        self.current_sequence = self.hero_system.generate_sequence(self.current_round)
        self.sequence_step = 0
        self.sequence_complete = False
        self.monster_health = 15
        self.hero_progress = 0
        self.combo_count = 0
        self.perfect_count = 0
        self.score = 0
        self.current_round = 1
        
        self.hero_system.show_sequence_prompt(self.current_round, self.sequence_step, self.current_sequence)
        self.current_timer = self.max_timer
        self.display_system.update_score(self.current_round, self.sequence_step, self.current_sequence)
        
    def process_input(self, key):
        if self.current_mode != "hero_sequence" or self.sequence_complete:
            return
            
        expected_key = self.current_sequence[self.sequence_step]
        
        # 检查时间奖励
        time_bonus = ""
        if self.current_timer > self.max_timer * 0.7:
            time_bonus = "PERFECT! "
            self.perfect_count += 1
            self.hero_system.show_feedback(f"{time_bonus}+50 BONUS", "gold")
            self.score += 50
            self.manager.add_score(50)  # 添加到游戏分数
        elif self.current_timer > self.max_timer * 0.3:
            time_bonus = "GOOD! "
            self.hero_system.show_feedback(f"{time_bonus}+25 BONUS", "green")
            self.score += 25
            self.manager.add_score(25)  # 添加到游戏分数
        
        if key == expected_key:
            # 正确输入
            self.sequence_step += 1
            self.combo_count += 1
            self.hero_progress += 25
            
            # 播放特效和怪物受伤动画
            self.hero_system.show_monster("hurt")
            
            # 根据按键播放不同特效
            if key in ["A", "S"]:
                self.hero_system.show_sword_effect()
            elif key in ["D", "F"]:
                self.hero_system.show_gun_effect()
            elif key in ["J", "K"]:
                self.hero_system.show_fist_effect()
            elif key == "L":
                if self.current_round == 1:
                    self.hero_system.show_magic_effect()
                else:
                    self.hero_system.show_arrow_effect()
            
            self.monster_health -= 1
            self.hero_system.show_health_bar(self.monster_health)
            
            if self.sequence_step >= len(self.current_sequence):
                # 当前轮次完成
                if self.current_round < self.total_sequences:
                    # 进入下一轮
                    self.current_round += 1
                    self.sequence_step = 0
                    self.current_sequence = self.hero_system.generate_sequence(self.current_round)
                    self.hero_system.show_feedback(f"ROUND {self.current_round} COMPLETE!", "cyan")
                    self.transition_timer = 90
                    self.current_mode = "round_transition"
                else:
                    # 所有轮次完成
                    self.sequence_complete = True
                    self.transition_timer = 60
                    self.hero_system.show_finisher_effect()
                    self.hero_system.show_monster("defeated")
                    self.display_system.update_state("FLAWLESS VICTORY!")
            else:
                # 显示下一个按键提示
                self.current_timer = self.max_timer
                self.hero_system.show_sequence_prompt(self.current_round, self.sequence_step, self.current_sequence)
        else:
            # 错误输入 - 怪物反击（但不会失败）
            self.combo_count = 0
            self.hero_system.show_monster("attack")
            self.hero_system.show_feedback("WRONG KEY! MONSTER ATTACKS!", "red")
            # 重置计时器，让玩家继续尝试
            self.current_timer = self.max_timer
            
    def start_victory_celebration(self):
        self.current_mode = "victory"
        self.transition_timer = 180
        
        # 确保清除所有特效
        self.hero_system.clear_all()
        self.show_blue_tombstone()
        self.firework_system.create_victory_fireworks()
        
        # 显示最终分数
        bonus = self.perfect_count * 50 + ((self.total_sequences * len(self.current_sequence)) - self.perfect_count) * 25
        total_score = self.score + bonus
        self.display_system.update_state(f"FINAL SCORE: {total_score}! PRESS R FOR TITLE")
        
        # 在显示蓝色墓碑时保存游戏状态
        self.manager.save_data.blue_completed = True
        # 更新历史总分
        if self.manager.session_total_score > self.manager.save_data.historical_total:
            self.manager.save_data.historical_total = self.manager.session_total_score
        SaveManager.save_game(self.manager.save_data)
        
    def show_blue_tombstone(self):
        """显示蓝色墓碑 - 仿照紫色墓碑格式"""
        tombstone = turtle.Turtle()
        tombstone.hideturtle()
        tombstone.penup()
        tombstone.color("blue")  # 蓝色墓碑
        tombstone.goto(0, 50)
        
        tombstone_art = [
            "  _____________",
            " |             |",
            " |   REST IN   |", 
            " |    PEACE    |",
            " |             |",
            " |     Mike    |",
            " |  1999-2025  |",
            " |_____________|",
            "      |   |",
            "      |   |",
            "     _|___|_"
        ]
        
        for i, line in enumerate(tombstone_art):
            tombstone.goto(-90, 100 - i * 20)
            tombstone.write(line, align="left", font=("Courier", 12, "normal"))
            
        # 墓碑上的文字 - 蓝色
        epitaph = turtle.Turtle()
        epitaph.hideturtle()
        epitaph.penup()
        epitaph.color("blue")  # 蓝色文字
        epitaph.goto(0, -150)
        epitaph.write("Hero Mike rests here, his spirit lives on forever", 
                     align="center", font=("Arial", 14, "normal"))
        
        # 新增CODE-ALEX文字 - 蓝色
        code_alex = turtle.Turtle()
        code_alex.hideturtle()
        code_alex.penup()
        code_alex.color("blue")  # 蓝色文字
        code_alex.goto(0, -180)
        code_alex.write("CODE-ALEX", align="center", font=("Arial", 14, "bold"))
        
        self.screen.update()
        
    def restart_to_title(self):
        """返回标题"""
        self.manager.reset_game_score()
        self.manager.change_state(GameState.TITLE)
        
    def run(self):
        """运行QTE游戏"""
        self.clear_screen()
        self.manager.score_display.update()
        
        # 初始化系统
        self.hero_system.setup()
        self.display_system.setup()
        
        # 直接开始游戏，跳过标题显示
        self.start_game()
        
        # 绑定按键
        self.screen.listen()
        self.screen.onkeypress(self.restart_to_title, "r")
        self.screen.onkeypress(self.restart_to_title, "R")
        
        # 绑定QTE按键
        self.screen.listen()
        self.screen.onkeypress(lambda: self.process_input("A"), "a")
        self.screen.onkeypress(lambda: self.process_input("A"), "A")
        self.screen.onkeypress(lambda: self.process_input("S"), "s")
        self.screen.onkeypress(lambda: self.process_input("S"), "S")
        self.screen.onkeypress(lambda: self.process_input("D"), "d")
        self.screen.onkeypress(lambda: self.process_input("D"), "D")
        self.screen.onkeypress(lambda: self.process_input("F"), "f")
        self.screen.onkeypress(lambda: self.process_input("F"), "F")
        self.screen.onkeypress(lambda: self.process_input("J"), "j")
        self.screen.onkeypress(lambda: self.process_input("J"), "J")
        self.screen.onkeypress(lambda: self.process_input("K"), "k")
        self.screen.onkeypress(lambda: self.process_input("K"), "K")
        self.screen.onkeypress(lambda: self.process_input("L"), "l")
        self.screen.onkeypress(lambda: self.process_input("L"), "L")
        self.screen.onkeypress(self.restart_to_title, "r")
        self.screen.onkeypress(self.restart_to_title, "R")
        
        # 游戏主循环
        while self.manager.current_state == GameState.BLUE_QTE:
            self.screen.update()
            
            if self.current_mode == "hero_intro":
                self.transition_timer -= 1
                if self.transition_timer <= 0:
                    self.start_hero_sequence()
                    
            elif self.current_mode == "hero_sequence":
                if not self.sequence_complete:
                    # 更新倒计时（仅用于视觉效果，不会导致失败）
                    self.current_timer -= 1
                    self.hero_system.show_timer(self.current_timer)
                    self.display_system.update_combo(self.combo_count)
                    self.display_system.update_score(self.current_round, self.sequence_step, self.current_sequence)
                    
                    # 检查超时（不会导致失败，只重置计时器）
                    if self.current_timer <= 0:
                        self.hero_system.show_feedback("TOO SLOW! TRY AGAIN!", "orange")
                        self.current_timer = self.max_timer  # 重置计时器
                else:
                    self.transition_timer -= 1
                    if self.transition_timer <= 0:
                        self.start_victory_celebration()
                        
            elif self.current_mode == "round_transition":
                self.transition_timer -= 1
                if self.transition_timer <= 0:
                    self.current_timer = self.max_timer
                    self.hero_system.show_sequence_prompt(self.current_round, self.sequence_step, self.current_sequence)
                    self.current_mode = "hero_sequence"
                    
            elif self.current_mode == "victory":
                self.firework_system.update_fireworks()
                self.transition_timer -= 1
                if self.transition_timer <= 0:
                    self.display_system.update_state("PRESS R TO RETURN TO TITLE")
                    self.current_mode = "victory_waiting"
                    
            elif self.current_mode == "victory_waiting":
                # 等待玩家按R
                pass
            
            time.sleep(0.05)

# QTE游戏的子系统
class HeroSystem:
    def __init__(self):
        self.hero_display = None
        self.monster_display = None
        self.instruction_display = None
        self.timer_display = None
        self.effect_display = None
        self.feedback_display = None
        self.sequence_keys = ["A", "S", "D", "F", "J", "K", "L"]
        self.active_effects = []
        
    def setup(self):
        self.hero_display = turtle.Turtle()
        self.hero_display.speed(0)
        self.hero_display.color("#00FF00")
        self.hero_display.penup()
        self.hero_display.hideturtle()
        
        self.monster_display = turtle.Turtle()
        self.monster_display.speed(0)
        self.monster_display.color("#FF0000")
        self.monster_display.penup()
        self.monster_display.hideturtle()
        
        self.instruction_display = turtle.Turtle()
        self.instruction_display.speed(0)
        self.instruction_display.color("yellow")
        self.instruction_display.penup()
        self.instruction_display.hideturtle()
        
        self.timer_display = turtle.Turtle()
        self.timer_display.speed(0)
        self.timer_display.color("white")
        self.timer_display.penup()
        self.timer_display.hideturtle()
        
        self.effect_display = turtle.Turtle()
        self.effect_display.speed(0)
        self.effect_display.color("cyan")
        self.effect_display.penup()
        self.effect_display.hideturtle()
        
        self.feedback_display = turtle.Turtle()
        self.feedback_display.speed(0)
        self.feedback_display.penup()
        self.feedback_display.hideturtle()
    
    def show_hero(self):
        self.hero_display.clear()
        self.hero_display.goto(-200, 0)
        
        hero_art = [
            "    O",
            "   /|\\",
            "   / \\",
            "  ======",
            "   | |",
            "  /   \\"
        ]
        
        for i, line in enumerate(hero_art):
            self.hero_display.goto(-200, 50 - i * 20)
            self.hero_display.write(line, align="left", font=("Courier", 14, "bold"))
    
    def show_monster(self, state="normal"):
        self.monster_display.clear()
        self.monster_display.goto(100, 0)
        
        if state == "normal":
            monster_art = [
                "   .-.          .-.",
                "  (o o) BOOM!  (o o)",
                "  | O \\        / O |",
                "  |   \\   __   /   |",
                "   \\   \\ (  ) /   /",
                "    \\   )    (   /",
                "     \\ /      \\ /",
                "      |        |",
                "     / \\      / \\",
                "    /   \\____/   \\"
            ]
        elif state == "hurt":
            monster_art = [
                "   .-.          .-.",
                "  (o o) OUCH!  (o o)",
                "  | O \\    💢  / O |",
                "  |   \\        /   |",
                "   \\   \\      /   /",
                "    \\   )    (   /",
                "     \\ /      \\ /",
                "      |   !!   |",
                "     / \\      / \\"
            ]
        elif state == "attack":
            monster_art = [
                "   .-.          .-.",
                "  (> <) GRR!  (> <)",
                "  | O \\ ====> / O |",
                "  |   \\        /   |",
                "   \\   \\      /   /",
                "    \\   )    (   /",
                "     \\ /      \\ /",
                "      |        |",
                "     / \\      / \\"
            ]
        elif state == "defeated":
            monster_art = [
                "   .-.          .-.",
                "  (x x) X_X   (x x)",
                "  | O \\        / O |",
                "  |   \\        /   |",
                "   \\   \\      /   /",
                "    \\   )    (   /",
                "     \\ /  ..  \\ /"
            ]
        
        for i, line in enumerate(monster_art):
            self.monster_display.goto(100, 80 - i * 15)
            self.monster_display.write(line, align="left", font=("Courier", 10, "bold"))
    
    def show_instruction(self, message, color="yellow"):
        self.instruction_display.clear()
        self.instruction_display.color(color)
        self.instruction_display.goto(0, -150)
        self.instruction_display.write(message, align="center", font=("Arial", 16, "bold"))
    
    def show_sequence_prompt(self, current_round, sequence_step, current_sequence):
        if sequence_step < len(current_sequence):
            current_key = current_sequence[sequence_step]
            self.show_instruction(f"ROUND {current_round}/3 - PRESS: {current_key}", "cyan")
    
    def show_timer(self, time_left):
        self.timer_display.clear()
        self.timer_display.goto(0, -120)
        
        if time_left > 60:
            self.timer_display.color("green")
        elif time_left > 30:
            self.timer_display.color("yellow")
        else:
            self.timer_display.color("red")
        
        progress = time_left / 90  # max_timer is 90
        bar_length = 20
        filled = int(bar_length * progress)
        bar = "█" * filled + "░" * (bar_length - filled)
        
        self.timer_display.write(f"[{bar}]", align="center", font=("Courier", 12, "bold"))
    
    def show_feedback(self, message, color="white"):
        self.feedback_display.clear()
        self.feedback_display.color(color)
        self.feedback_display.goto(0, 180)
        self.feedback_display.write(message, align="center", font=("Arial", 18, "bold"))
        
        def clear_feedback():
            self.feedback_display.clear()
        turtle.ontimer(clear_feedback, 2000)
    
    def generate_sequence(self, current_round):
        # 根据轮次增加难度
        if current_round == 1:
            return random.sample(["A", "S", "D", "F"], 4)
        elif current_round == 2:
            return random.sample(["A", "S", "D", "F", "J", "K"], 5)
        else:
            return random.sample(self.sequence_keys, 6)
    
    def show_sword_effect(self):
        """剑特效 - 使用turtle绘图"""
        effect = turtle.Turtle()
        effect.speed(0)
        effect.color("silver")
        effect.pensize(3)
        effect.penup()
        effect.goto(-150, 0)
        effect.pendown()
        
        # 绘制剑的形状
        effect.forward(100)  # 剑身
        effect.left(150)
        effect.forward(20)   # 剑柄
        effect.backward(40)
        effect.forward(20)
        effect.right(150)
        
        effect.penup()
        effect.goto(-100, 30)
        effect.color("cyan")
        effect.write("SWORD SLASH!", align="center", font=("Arial", 14, "bold"))
        
        # 动画效果 - 剑飞向怪物
        def animate_sword(step=0):
            if step < 15:
                effect.clear()
                effect.penup()
                effect.goto(-150 + step * 20, 0)
                effect.pendown()
                
                # 重新绘制剑
                effect.color("silver")
                effect.forward(50)
                effect.left(150)
                effect.forward(10)
                effect.backward(20)
                effect.forward(10)
                effect.right(150)
                
                turtle.ontimer(lambda: animate_sword(step + 1), 50)
            else:
                effect.clear()
                effect.hideturtle()
        
        animate_sword()
    
    def show_gun_effect(self):
        """枪特效 - 使用turtle绘图"""
        effect = turtle.Turtle()
        effect.speed(0)
        effect.color("orange")
        effect.penup()
        effect.hideturtle()
        
        bullets = []
        # 创建多个子弹
        for i in range(5):
            bullet = turtle.Turtle()
            bullet.speed(0)
            bullet.shape("circle")
            bullet.color("yellow")
            bullet.shapesize(0.3)
            bullet.penup()
            bullet.goto(-180 + i * 10, -10 + i * 5)
            bullets.append(bullet)
        
        effect.goto(-120, 30)
        effect.write("GATLING GUN!", align="center", font=("Arial", 14, "bold"))
        
        # 子弹动画
        def animate_bullets(step=0):
            if step < 20:
                for i, bullet in enumerate(bullets):
                    bullet.forward(15)
                turtle.ontimer(lambda: animate_bullets(step + 1), 30)
            else:
                for bullet in bullets:
                    bullet.hideturtle()
                effect.clear()
                effect.hideturtle()
        
        animate_bullets()
    
    def show_fist_effect(self):
        """拳头特效 - 使用turtle绘图"""
        effect = turtle.Turtle()
        effect.speed(0)
        effect.color("brown")
        effect.pensize(4)
        effect.penup()
        effect.goto(-120, 0)
        
        # 绘制拳头
        effect.pendown()
        effect.circle(15)  # 拳头主体
        
        effect.penup()
        effect.goto(-100, 30)
        effect.color("red")
        effect.write("MEGA FIST!", align="center", font=("Arial", 14, "bold"))
        
        # 冲击波动画
        shockwaves = []
        def animate_shockwave(step=0):
            if step < 10:
                shockwave = turtle.Turtle()
                shockwave.speed(0)
                shockwave.color("red")
                shockwave.pensize(2)
                shockwave.penup()
                shockwave.goto(-80 + step * 15, 0)
                shockwave.pendown()
                shockwave.circle(10 + step * 3)
                shockwave.hideturtle()
                shockwaves.append(shockwave)
                
                turtle.ontimer(lambda: animate_shockwave(step + 1), 100)
            else:
                # 清除所有冲击波
                for shockwave in shockwaves:
                    shockwave.clear()
                    shockwave.hideturtle()
                effect.clear()
                effect.hideturtle()
        
        animate_shockwave()
    
    def show_magic_effect(self):
        """魔法特效 - 使用turtle绘图"""
        effect = turtle.Turtle()
        effect.speed(0)
        effect.color("purple")
        effect.penup()
        effect.goto(-120, 0)
        
        # 绘制魔法阵
        effect.pendown()
        for i in range(6):
            effect.forward(20)
            effect.backward(20)
            effect.left(60)
        
        effect.penup()
        effect.goto(-100, 30)
        effect.color("magenta")
        effect.write("MAGIC BLAST!", align="center", font=("Arial", 14, "bold"))
        
        # 魔法粒子效果
        particles = []
        for i in range(8):
            particle = turtle.Turtle()
            particle.speed(0)
            particle.shape("circle")
            particle.color("cyan")
            particle.shapesize(0.4)
            particle.penup()
            particle.goto(-120, 0)
            particles.append(particle)
        
        def animate_particles(step=0):
            if step < 15:
                for i, particle in enumerate(particles):
                    angle = i * 45
                    distance = step * 8
                    x = -120 + math.cos(math.radians(angle)) * distance
                    y = math.sin(math.radians(angle)) * distance
                    particle.goto(x, y)
                turtle.ontimer(lambda: animate_particles(step + 1), 50)
            else:
                for particle in particles:
                    particle.hideturtle()
                effect.clear()
                effect.hideturtle()
        
        animate_particles()
    
    def show_arrow_effect(self):
        """箭特效 - 使用turtle绘图"""
        effect = turtle.Turtle()
        effect.speed(0)
        effect.color("green")
        effect.pensize(2)
        effect.penup()
        effect.goto(-180, 0)
        
        # 绘制箭头
        effect.pendown()
        effect.forward(40)  # 箭杆
        effect.left(150)
        effect.forward(10)  # 箭头
        effect.backward(10)
        effect.right(300)
        effect.forward(10)
        
        effect.penup()
        effect.goto(-140, 30)
        effect.color("green")
        effect.write("ARROW STORM!", align="center", font=("Arial", 14, "bold"))
        
        # 箭飞行动画
        def animate_arrow(step=0):
            if step < 18:
                effect.clear()
                effect.penup()
                effect.goto(-180 + step * 15, 0)
                effect.pendown()
                
                # 重新绘制箭
                effect.color("green")
                effect.forward(30)
                effect.left(150)
                effect.forward(8)
                effect.backward(8)
                effect.right(300)
                effect.forward(8)
                
                turtle.ontimer(lambda: animate_arrow(step + 1), 40)
            else:
                effect.clear()
                effect.hideturtle()
        
        animate_arrow()
    
    def show_finisher_effect(self):
        """终结技特效 - 使用turtle绘图"""
        effect = turtle.Turtle()
        effect.speed(0)
        effect.color("gold")
        effect.penup()
        effect.goto(0, 0)
        
        # 绘制爆炸效果
        def draw_explosion():
            effect.pendown()
            for i in range(8):
                effect.forward(30)
                effect.backward(30)
                effect.left(45)
            effect.penup()
        
        draw_explosion()
        
        effect.goto(0, 50)
        effect.write("ULTIMATE FINISHER!", align="center", font=("Arial", 16, "bold"))
        
        # 多重爆炸动画
        explosions = []
        def animate_explosion(step=0):
            if step < 5:
                effect.clear()
                effect.penup()
                effect.goto(0, 0)
                
                # 绘制不同大小的爆炸
                size = 20 + step * 10
                effect.pendown()
                for i in range(8):
                    effect.forward(size)
                    effect.backward(size)
                    effect.left(45)
                effect.penup()
                
                effect.goto(0, 50)
                effect.write("ULTIMATE FINISHER!", align="center", font=("Arial", 16, "bold"))
                
                turtle.ontimer(lambda: animate_explosion(step + 1), 200)
            else:
                effect.clear()
                effect.hideturtle()
        
        animate_explosion()
    
    def show_health_bar(self, monster_health):
        health_display = turtle.Turtle()
        health_display.speed(0)
        health_display.color("red")
        health_display.penup()
        health_display.hideturtle()
        health_display.goto(100, 150)
        
        health_bar = "█" * monster_health + "░" * (15 - monster_health)
        health_display.write(f"MONSTER HP: [{health_bar}]", align="center", font=("Courier", 10, "bold"))
        
        def clear_health():
            health_display.clear()
            health_display.hideturtle()
        turtle.ontimer(clear_health, 1000)
    
    def clear_all(self):
        """清除所有显示内容"""
        self.hero_display.clear()
        self.monster_display.clear()
        self.instruction_display.clear()
        self.timer_display.clear()
        self.effect_display.clear()
        self.feedback_display.clear()

class FireworkSystem:
    def __init__(self):
        self.fireworks = []
        
    def create_firework(self, x, y, color):
        firework = {
            'x': x,
            'y': y,
            'color': color,
            'particles': [],
            'exploded': False,
            'timer': random.randint(20, 40)
        }
        
        for i in range(5):
            particle = turtle.Turtle()
            particle.speed(0)
            particle.shape("circle")
            particle.color(color)
            particle.penup()
            particle.goto(x, y - i * 3)
            particle.turtlesize(0.3)
            firework['particles'].append(particle)
        
        self.fireworks.append(firework)
    
    def update_fireworks(self):
        for firework in self.fireworks[:]:
            if not firework['exploded']:
                for particle in firework['particles']:
                    particle.sety(particle.ycor() + 4)
                
                firework['timer'] -= 1
                if firework['timer'] <= 0:
                    self.explode_firework(firework)
            else:
                for particle in firework['particles'][:]:
                    particle.setx(particle.xcor() + particle.dx)
                    particle.sety(particle.ycor() + particle.dy)
                    particle.dy -= 0.2
                    
                    current_size = particle.turtlesize()[0]
                    if current_size > 0.05:
                        particle.turtlesize(current_size * 0.95)
                    else:
                        particle.hideturtle()
                        firework['particles'].remove(particle)
                
                if len(firework['particles']) == 0:
                    self.fireworks.remove(firework)
    
    def explode_firework(self, firework):
        firework['exploded'] = True
        x, y = firework['particles'][0].xcor(), firework['particles'][0].ycor()
        color = firework['color']
        
        for particle in firework['particles']:
            particle.hideturtle()
        
        firework['particles'] = []
        
        for _ in range(30):
            particle = turtle.Turtle()
            particle.speed(0)
            particle.shape("circle")
            particle.color(color)
            particle.penup()
            particle.goto(x, y)
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(2, 6)
            particle.dx = math.cos(angle) * speed
            particle.dy = math.sin(angle) * speed
            particle.turtlesize(random.uniform(0.3, 0.8))
            firework['particles'].append(particle)
    
    def create_victory_fireworks(self):
        colors = ["red", "blue", "green", "yellow", "purple", "cyan", "orange"]
        for _ in range(20):
            x = random.randint(-250, 250)
            y = random.randint(-200, 0)
            color = random.choice(colors)
            self.create_firework(x, y, color)
    
    def clear_fireworks(self):
        for firework in self.fireworks:
            for particle in firework['particles']:
                particle.hideturtle()
        self.fireworks.clear()

class TombstoneSystem:
    def __init__(self):
        self.tombstone_display = turtle.Turtle()
        self.tombstone_display.speed(0)
        self.tombstone_display.color("blue")
        self.tombstone_display.penup()
        self.tombstone_display.hideturtle()
        
    def show_blue_tombstone(self):
        self.tombstone_display.clear()
        self.tombstone_display.goto(0, 50)
        
        tombstone_art = [
            "  _____________",
            " |             |",
            " |   REST IN   |", 
            " |    PEACE    |",
            " |             |",
            " |     Mike    |",
            " |  1999-2025  |",
            " |_____________|",
            "      |   |",
            "      |   |",
            "     _|___|_"
        ]
        
        for i, line in enumerate(tombstone_art):
            self.tombstone_display.goto(-90, 100 - i * 20)
            self.tombstone_display.write(line, align="left", font=("Courier", 12, "normal"))
        
        # 墓碑上的文字 - 蓝色
        epitaph = turtle.Turtle()
        epitaph.hideturtle()
        epitaph.penup()
        epitaph.color("blue")
        epitaph.goto(0, -150)
        epitaph.write("Hero Mike rests here, his spirit lives on forever", 
                     align="center", font=("Arial", 14, "normal"))
        
        # 新增CODE-ALEX文字 - 蓝色
        code_alex = turtle.Turtle()
        code_alex.hideturtle()
        code_alex.penup()
        code_alex.color("blue")
        code_alex.goto(0, -180)
        code_alex.write("CODE-ALEX", align="center", font=("Arial", 14, "bold"))
        
        self.tombstone_display.screen.update()
    
    def hide_tombstone(self):
        self.tombstone_display.clear()

class DisplaySystem:
    def __init__(self):
        self.score_display = None
        self.state_display = None
        self.combo_display = None
        
    def setup(self):
        self.score_display = turtle.Turtle()
        self.score_display.speed(0)
        self.score_display.color("white")
        self.score_display.penup()
        self.score_display.hideturtle()
        self.score_display.goto(0, 260)
        
        self.state_display = turtle.Turtle()
        self.state_display.speed(0)
        self.state_display.color("white")
        self.state_display.penup()
        self.state_display.hideturtle()
        self.state_display.goto(0, 230)
        
        self.combo_display = turtle.Turtle()
        self.combo_display.speed(0)
        self.combo_display.color("gold")
        self.combo_display.penup()
        self.combo_display.hideturtle()
        self.combo_display.goto(-280, 230)
    
    def update_score(self, current_round, sequence_step, current_sequence):
        self.score_display.clear()
        attacks_left = len(current_sequence) - sequence_step
        self.score_display.write(f"ROUND {current_round}/3 - ATTACKS: {attacks_left}/{len(current_sequence)}", align="center", font=("Arial", 16, "normal"))
    
    def update_combo(self, combo_count):
        self.combo_display.clear()
        if combo_count > 1:
            self.combo_display.write(f"COMBO: x{combo_count}", align="left", font=("Arial", 14, "bold"))
    
    def update_state(self, message=""):
        self.state_display.clear()
        if message:
            self.state_display.write(message, align="center", font=("Arial", 14, "normal"))
    
    def clear_all(self):
        self.score_display.clear()
        self.state_display.clear()
        self.combo_display.clear()