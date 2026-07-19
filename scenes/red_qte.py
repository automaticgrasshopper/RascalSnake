import turtle
import time
import random
import math
from scenes.base_scene import BaseScene
from constants import GameState

class RedQTE(BaseScene):
    def __init__(self, game_manager):
        super().__init__(game_manager)
        self.score = 0
        self.game_over = False
        self.current_mode = "intro"
        self.transition_timer = 120
        self.game_started = True
        self.monster_progress = 0
        self.sequence_step = 0
        self.current_sequence = []
        self.sequence_complete = False
        self.human_health = 15
        self.current_timer = 0
        self.max_timer = 90
        self.perfect_count = 0
        self.total_sequences = 3
        self.current_round = 1
        self.effects = []  # 存储特效对象
        
        # 调整画幅参数
        self.screen_width = 800
        self.screen_height = 600
        self.center_x = 0
        self.center_y = 0
        
        # 创建显示对象
        self.health_display = None
        self.timer_display = None
        self.prompt_display = None
        self.feedback_display = None
        
    def setup_displays(self):
        """设置显示对象"""
        # 血量显示
        self.health_display = turtle.Turtle()
        self.health_display.speed(0)
        self.health_display.color("red")
        self.health_display.penup()
        self.health_display.hideturtle()
        
        # 计时器显示
        self.timer_display = turtle.Turtle()
        self.timer_display.speed(0)
        self.timer_display.penup()
        self.timer_display.hideturtle()
        
        # 提示显示
        self.prompt_display = turtle.Turtle()
        self.prompt_display.speed(0)
        self.prompt_display.color("cyan")
        self.prompt_display.penup()
        self.prompt_display.hideturtle()
        
        # 反馈显示
        self.feedback_display = turtle.Turtle()
        self.feedback_display.speed(0)
        self.feedback_display.penup()
        self.feedback_display.hideturtle()
        
    def adjust_positions(self):
        """调整所有元素的位置以适应画幅，确保在屏幕中心显示"""
        # 怪物位置 - 抬高一些，底部与按键提示相距半格高度
        self.monster_x = 150
        self.monster_y = 80  # 从0抬高到80
        
        # 人类位置 - 放在左侧
        self.human_blue_x = -200
        self.human_blue_y = 50
        self.human_purple_x = -200
        self.human_purple_y = -50
        
        # 特效起始位置 - 在怪物和小人中间
        self.effect_start_x = -25  # 在怪物(150)和小人(-200)中间
        self.effect_start_y = 40   # 在怪物(80)和小人(50/-50)中间
        
        # 提示信息位置 - 确保在屏幕范围内
        self.prompt_y = -180
        self.timer_y = -150
        self.feedback_y = 200
        self.health_y = 150
        
        # QTE按键提示位置 - 放在屏幕中心下方
        self.qte_prompt_y = -120
        
    def create_monster(self):
        """创建怪物 - 调整位置适应画幅"""
        self.adjust_positions()
        
        monster = turtle.Turtle()
        monster.hideturtle()
        monster.penup()
        monster.color("red")
        monster.goto(self.monster_x, self.monster_y)
        
        # ASCII 怪物艺术 - 调整大小使其适合屏幕
        monster_art = [
            "        ______________",
            "  ,===:'.,            `-._",
            "         `:.`---.__         `-._",
            "           `:.     `--.         `.",
            "             \\.        `.         `.",
            "     (,,(,    \\.         `.   ____,-`.,",
            "  (,'     `/   \\.   ,--.___`.'",
            ",  ,'  ,--.  `,   \\.;'         `",
            " `{D, {    \\  :    \\;",
            "   V,,'    /  /    //",
            "   j;;    /  ,' ,-//.    ,---.      ,",
            "   \\;'   /  ,' /  _  \\  /  _  \\   ,'/",
            "         \\   `'  / \\  `'  / \\  `.' /",
            "          `.___,'   `.__,'   `.__,'"
        ]
        
        for i, line in enumerate(monster_art):
            monster.goto(self.monster_x - 50, self.monster_y + 80 - i * 18)  # 调整位置
            monster.write(line, align="left", font=("Courier", 7, "normal"))
            
        return monster
        
    def create_humans(self):
        """创建两个小人 - 调整位置适应画幅"""
        self.adjust_positions()
        
        humans = []
        
        # 蓝色小人
        blue_human = turtle.Turtle()
        blue_human.hideturtle()
        blue_human.penup()
        blue_human.color("blue")
        blue_human.goto(self.human_blue_x, self.human_blue_y)
        
        blue_art = [
            "    O",
            "   /|\\",
            "   / \\"
        ]
        
        for i, line in enumerate(blue_art):
            blue_human.goto(self.human_blue_x, self.human_blue_y + 30 - i * 20)
            blue_human.write(line, align="left", font=("Courier", 10, "normal"))
            
        # 紫色小人  
        purple_human = turtle.Turtle()
        purple_human.hideturtle()
        purple_human.penup()
        purple_human.color("#8A2BE2")
        purple_human.goto(self.human_purple_x, self.human_purple_y)
        
        purple_art = [
            "    O",
            "   /|\\", 
            "   / \\"
        ]
        
        for i, line in enumerate(purple_art):
            purple_human.goto(self.human_purple_x, self.human_purple_y + 30 - i * 20)
            purple_human.write(line, align="left", font=("Courier", 10, "normal"))
            
        humans.extend([blue_human, purple_human])
        return humans
        
    def create_monster_effect(self, effect_type):
        """创建怪物特效 - 从中间位置向小人发射"""
        self.adjust_positions()
        
        effects = []
        
        if effect_type == "spark":
            # 火花特效 - 从中间位置发射
            for _ in range(15):
                spark = turtle.Turtle()
                spark.speed(0)
                spark.shape("circle")
                spark.color(random.choice(["red", "orange", "yellow"]))
                spark.penup()
                spark.goto(self.effect_start_x, self.effect_start_y)  # 从中间位置发射
                spark.shapesize(0.5, 0.5)
                spark.showturtle()  # 确保可见
                
                # 向小人方向发射
                target_x = random.choice([self.human_blue_x, self.human_purple_x])
                target_y = random.choice([self.human_blue_y, self.human_purple_y])
                
                # 计算方向向量
                dx = target_x - self.effect_start_x
                dy = target_y - self.effect_start_y
                distance = math.sqrt(dx*dx + dy*dy)
                
                # 标准化并设置速度
                speed = random.uniform(3, 6)
                vx = (dx / distance) * speed
                vy = (dy / distance) * speed
                
                lifespan = random.randint(20, 30)
                
                effects.append((spark, vx, vy, lifespan))
                
        elif effect_type == "lightning":
            # 闪电特效 - 从中间位置发射
            for _ in range(5):
                lightning = turtle.Turtle()
                lightning.speed(0)
                lightning.shape("triangle")
                lightning.color("cyan")
                lightning.penup()
                lightning.goto(self.effect_start_x, self.effect_start_y)  # 从中间位置发射
                lightning.shapesize(0.5, 1.0)
                lightning.showturtle()  # 确保可见
                
                # 向小人方向发射
                target_x = random.choice([self.human_blue_x, self.human_purple_x])
                target_y = random.choice([self.human_blue_y, self.human_purple_y])
                
                # 计算方向
                dx = target_x - self.effect_start_x
                dy = target_y - self.effect_start_y
                distance = math.sqrt(dx*dx + dy*dy)
                
                # 标准化并设置速度
                speed = random.uniform(4, 7)
                vx = (dx / distance) * speed
                vy = (dy / distance) * speed
                
                # 设置朝向
                angle = math.degrees(math.atan2(dy, dx))
                lightning.setheading(angle)
                
                lifespan = random.randint(15, 25)
                
                effects.append((lightning, vx, vy, lifespan))
                
        elif effect_type == "explosion":
            # 爆炸特效 - 从中间位置发射
            for _ in range(20):
                particle = turtle.Turtle()
                particle.speed(0)
                particle.shape("circle")
                particle.color(random.choice(["red", "orange", "yellow"]))
                particle.penup()
                particle.goto(self.effect_start_x, self.effect_start_y)  # 从中间位置发射
                particle.shapesize(0.3, 0.3)
                particle.showturtle()  # 确保可见
                
                # 随机方向，但主要向左（向小人方向）
                angle = random.uniform(math.pi/2 + 0.5, math.pi*3/2 - 0.5)  # 主要向左
                speed = random.uniform(2, 5)
                vx = math.cos(angle) * speed
                vy = math.sin(angle) * speed
                lifespan = random.randint(20, 30)
                
                effects.append((particle, vx, vy, lifespan))
                
        return effects
        
    def update_effects(self):
        """更新特效，移除超出屏幕的特效"""
        updated_effects = []
        
        for effect in self.effects:
            obj, vx, vy, lifespan = effect
            
            # 更新位置
            x, y = obj.position()
            new_x = x + vx
            new_y = y + vy
            obj.goto(new_x, new_y)
            
            # 减少寿命
            lifespan -= 1
            
            # 如果还有寿命，保留特效
            if lifespan > 0:
                # 逐渐变小
                current_size = obj.shapesize()[0]
                if current_size > 0.05:
                    obj.shapesize(current_size * 0.95, current_size * 0.95)
                    updated_effects.append((obj, vx, vy, lifespan))
                else:
                    obj.hideturtle()
            else:
                obj.hideturtle()
                
        self.effects = updated_effects
        
    def start_game(self):
        """开始游戏"""
        self.current_mode = "qte_sequence"
        self.start_sequence()
        
    def start_sequence(self):
        """开始QTE序列"""
        self.current_sequence = self.generate_sequence(self.current_round)
        self.sequence_step = 0
        self.sequence_complete = False
        self.human_health = 15
        self.monster_progress = 0
        self.perfect_count = 0
        self.score = 0
        
        self.show_sequence_prompt()
        self.current_timer = self.max_timer
        
    def generate_sequence(self, current_round):
        """生成QTE序列"""
        keys = ["A", "S", "D", "F", "J", "K", "L"]
        if current_round == 1:
            return random.sample(keys[:4], 4)
        elif current_round == 2:
            return random.sample(keys[:6], 5)
        else:
            return random.sample(keys, 6)
            
    def show_sequence_prompt(self):
        """显示QTE提示 - 持续显示直到下一个按键"""
        if self.sequence_step < len(self.current_sequence):
            current_key = self.current_sequence[self.sequence_step]
            
            self.prompt_display.clear()
            self.prompt_display.color("cyan")
            self.prompt_display.goto(0, self.qte_prompt_y)
            self.prompt_display.write(f"ROUND {self.current_round}/3 - PRESS: {current_key}", 
                                    align="center", font=("Arial", 16, "bold"))
            
    def show_timer(self):
        """显示计时器 - 持续显示"""
        self.timer_display.clear()
        self.timer_display.goto(0, self.timer_y)
        
        if self.current_timer > 60:
            self.timer_display.color("green")
        elif self.current_timer > 30:
            self.timer_display.color("yellow")
        else:
            self.timer_display.color("red")
            
        progress = self.current_timer / self.max_timer
        bar_length = 20
        filled = int(bar_length * progress)
        bar = "█" * filled + "░" * (bar_length - filled)
        
        self.timer_display.write(f"[{bar}]", align="center", font=("Courier", 12, "bold"))
        
    def show_feedback(self, message, color="white"):
        """显示反馈信息 - 持续显示2秒"""
        self.feedback_display.clear()
        self.feedback_display.color(color)
        self.feedback_display.goto(0, self.feedback_y)
        self.feedback_display.write(message, align="center", font=("Arial", 18, "bold"))
        
        # 2秒后清除反馈
        def clear_feedback():
            self.feedback_display.clear()
        turtle.ontimer(clear_feedback, 2000)
        
    def show_health_bar(self):
        """显示生命条 - 持续显示"""
        self.health_display.clear()
        self.health_display.color("red")
        self.health_display.goto(0, self.health_y)
        
        health_bar = "█" * self.human_health + "░" * (15 - self.human_health)
        self.health_display.write(f"HUMAN HP: [{health_bar}]", align="center", font=("Courier", 10, "bold"))
        
    def process_input(self, key):
        """处理按键输入"""
        if self.current_mode != "qte_sequence" or self.sequence_complete:
            return
            
        expected_key = self.current_sequence[self.sequence_step]
        
        # 检查时间奖励
        time_bonus = ""
        if self.current_timer > self.max_timer * 0.7:
            time_bonus = "PERFECT! "
            self.perfect_count += 1
            self.show_feedback(f"{time_bonus}+50 BONUS", "gold")
            self.score += 50
            self.manager.add_score(50)
        elif self.current_timer > self.max_timer * 0.3:
            time_bonus = "GOOD! "
            self.show_feedback(f"{time_bonus}+25 BONUS", "green")
            self.score += 25
            self.manager.add_score(25)
        
        if key == expected_key:
            # 正确输入 - 添加怪物特效
            effect_type = random.choice(["spark", "lightning", "explosion"])
            new_effects = self.create_monster_effect(effect_type)
            self.effects.extend(new_effects)
            
            self.sequence_step += 1
            
            # 人类受伤动画
            self.show_human_hurt()
            
            self.human_health -= 1
            self.show_health_bar()
            
            if self.sequence_step >= len(self.current_sequence):
                # 当前轮次完成
                if self.current_round < self.total_sequences:
                    # 进入下一轮
                    self.current_round += 1
                    self.sequence_step = 0
                    self.current_sequence = self.generate_sequence(self.current_round)
                    self.show_feedback(f"ROUND {self.current_round} COMPLETE!", "cyan")
                    self.transition_timer = 90
                    self.current_mode = "round_transition"
                else:
                    # 所有轮次完成
                    self.sequence_complete = True
                    self.transition_timer = 60
                    self.show_finisher_effect()
                    self.show_human_defeated()
            else:
                # 显示下一个按键提示
                self.current_timer = self.max_timer
                self.show_sequence_prompt()
        else:
            # 错误输入
            self.show_human_attack()
            self.show_feedback("WRONG KEY! HUMAN FIGHTS BACK!", "red")
            self.current_timer = self.max_timer
            
    def show_human_hurt(self):
        """显示人类受伤"""
        hurt_effect = turtle.Turtle()
        hurt_effect.hideturtle()
        hurt_effect.penup()
        hurt_effect.color("red")
        hurt_effect.goto(self.human_blue_x, 0)
        hurt_effect.write("OUCH!", align="center", font=("Arial", 14, "bold"))
        self.screen.ontimer(lambda: hurt_effect.clear(), 500)
        
    def show_human_attack(self):
        """显示人类反击"""
        attack_effect = turtle.Turtle()
        attack_effect.hideturtle()
        attack_effect.penup()
        attack_effect.color("blue")
        attack_effect.goto(self.human_blue_x, 0)
        attack_effect.write("FIGHT BACK!", align="center", font=("Arial", 14, "bold"))
        self.screen.ontimer(lambda: attack_effect.clear(), 500)
        
    def show_human_defeated(self):
        """显示人类被击败"""
        defeated = turtle.Turtle()
        defeated.hideturtle()
        defeated.penup()
        defeated.color("#808080")
        defeated.goto(self.human_blue_x, 0)
        defeated.write("DEFEATED", align="center", font=("Arial", 16, "bold"))
        
    def show_finisher_effect(self):
        """显示终结技特效"""
        # 创建大型爆炸特效 - 从小人位置发射
        for _ in range(30):
            particle = turtle.Turtle()
            particle.speed(0)
            particle.shape("circle")
            particle.color(random.choice(["red", "orange", "yellow", "white"]))
            particle.penup()
            particle.goto(self.human_blue_x, 0)  # 从小人位置发射
            particle.shapesize(0.5, 0.5)
            particle.showturtle()
            
            # 随机方向
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(3, 8)
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed
            lifespan = random.randint(30, 40)
            
            self.effects.append((particle, vx, vy, lifespan))
            
        finisher = turtle.Turtle()
        finisher.hideturtle()
        finisher.penup()
        finisher.color("red")
        finisher.goto(0, 0)
        finisher.write("FATALITY!", align="center", font=("Arial", 24, "bold"))
        self.screen.ontimer(lambda: finisher.clear(), 2000)
        
    def start_victory_celebration(self):
        """开始胜利庆祝"""
        self.current_mode = "victory"
        self.transition_timer = 180
        
        # 清除所有显示
        self.health_display.clear()
        self.timer_display.clear()
        self.prompt_display.clear()
        self.feedback_display.clear()
        
        # 显示胜利信息
        victory = turtle.Turtle()
        victory.hideturtle()
        victory.penup()
        victory.color("red")
        victory.goto(0, 0)
        victory.write("KILLER VICTORY!", align="center", font=("Arial", 24, "bold"))
        
        score_text = turtle.Turtle()
        score_text.hideturtle()
        score_text.penup()
        score_text.color("white")
        score_text.goto(0, -50)
        score_text.write(f"Final Score: {self.score}", align="center", font=("Arial", 16, "normal"))
        
        continue_text = turtle.Turtle()
        continue_text.hideturtle()
        continue_text.penup()
        continue_text.color("yellow")
        continue_text.goto(0, -100)
        continue_text.write("Loading...", align="center", font=("Arial", 16, "normal"))
        
        self.screen.update()
        time.sleep(2)
        self.manager.change_state(GameState.RED_ENDING)
        
    def restart_to_title(self):
        """返回标题"""
        self.manager.reset_game_score()
        self.manager.change_state(GameState.TITLE)
        
    def run(self):
        """运行红色QTE游戏 - 修复显示问题"""
        self.clear_screen()
        self.manager.score_display.update()
        
        # 设置显示对象
        self.setup_displays()
        
        # 调整画幅
        self.adjust_positions()
        
        # 直接创建游戏元素，不显示标题
        self.monster = self.create_monster()
        self.humans = self.create_humans()
        
        # 直接开始游戏，不显示标题界面
        self.start_game()
        
        # 绑定QTE按键
        self.screen.listen()
        for key in ["a", "A", "s", "S", "d", "D", "f", "F", "j", "J", "k", "K", "l", "L"]:
            self.screen.onkeypress(lambda k=key.upper(): self.process_input(k), key)
        self.screen.onkeypress(self.restart_to_title, "r")
        self.screen.onkeypress(self.restart_to_title, "R")
        
        # 游戏主循环
        while self.manager.current_state == GameState.RED_QTE:
            self.screen.update()
            
            # 更新特效
            self.update_effects()
            
            if self.current_mode == "qte_sequence":
                if not self.sequence_complete:
                    # 更新倒计时
                    self.current_timer -= 1
                    self.show_timer()
                    self.show_health_bar()
                    
                    # 检查超时
                    if self.current_timer <= 0:
                        self.show_feedback("TOO SLOW! TRY AGAIN!", "orange")
                        self.current_timer = self.max_timer
                else:
                    self.transition_timer -= 1
                    if self.transition_timer <= 0:
                        self.start_victory_celebration()
                        
            elif self.current_mode == "round_transition":
                self.transition_timer -= 1
                if self.transition_timer <= 0:
                    self.current_timer = self.max_timer
                    self.show_sequence_prompt()
                    self.current_mode = "qte_sequence"
                    
            time.sleep(0.05)