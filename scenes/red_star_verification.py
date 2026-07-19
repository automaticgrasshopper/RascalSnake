import turtle
import time
import math
from scenes.base_scene import BaseScene
from constants import GameState

class RedStarVerification(BaseScene):
    def __init__(self, game_manager):
        super().__init__(game_manager)
        self.blue_code = ""
        self.purple_code = ""
        self.current_input = "blue"  # 当前输入框：blue 或 purple
        self.verification_passed = False
        self.animation_complete = False
        
    def draw_demon_head(self):
        """绘制酷炫的ASCII魔鬼头"""
        demon_turtle = turtle.Turtle()
        demon_turtle.hideturtle()
        demon_turtle.penup()
        demon_turtle.color("#FF0000")  # 红色
        
        # 酷炫的ASCII魔鬼头
        demon_art = [
            "          .                                                      .",
            "        .n                   .                 .                  n.",
            "  .   .dP                  dP                   9b                 9b.    .",
            " 4    qXb         .       dX                     Xb       .        dXp     t",
            "dX.    9Xb      .dXb    __                         __    dXb.     dXP     .Xb",
            "9XXb._       _.dXXXXb dXXXXbo.                 .odXXXXb dXXXXb._       _.dXXP",
            " 9XXXXXXXXXXXXXXXXXXXVXXXXXXXXOo.           .oOXXXXXXXXVXXXXXXXXXXXXXXXXXXXP",
            "  `9XXXXXXXXXXXXXXXXXXXXX'~   ~`OOO8b   d8OOO'~   ~`XXXXXXXXXXXXXXXXXXXXXP'",
            "    `9XXXXXXXXXXXP' `9XX'   DIE    `98v8P'  HUMAN   `XXP' `9XXXXXXXXXXXP'",
            "        ~~~~~~~       9X.          .db|db.          .XP       ~~~~~~~",
            "                        )b.  .dbo.dP'`v'`9b.odb.  .dX(",
            "                      ,dXXXXXXXXXXXb     dXXXXXXXXXXXb.",
            "                     dXXXXXXXXXXXP'   .   `9XXXXXXXXXXXb",
            "                    dXXXXXXXXXXXXb   d|b   dXXXXXXXXXXXXb",
            "                    9XXb'   `XXXXXb.dX|Xb.dXXXXX'   `dXXP",
            "                     `'      9XXXXXX(   )XXXXXXP      `'",
            "                              XXXX X.`v'.X XXXX",
            "                              XP^X'`b   d'`X^XX",
            "                              X. 9  `   '  P )X",
            "                              `b  `       '  d'",
            "                               `             '"
        ]
        
        # 显示魔鬼头
        for i, line in enumerate(demon_art):
            demon_turtle.goto(-380, 200 - i * 20)
            demon_turtle.write(line, align="left", font=("Courier", 8, "bold"))
        
        self.screen.update()
        return demon_turtle
        
    def animate_hexagram_emergence(self):
        """六芒星从魔鬼头中出现的动画"""
        # 创建六芒星
        star = turtle.Turtle()
        star.speed(0)
        star.color("#FF4444")
        star.pensize(2)
        star.hideturtle()
        star.penup()
        
        # 六芒星从中心逐渐扩大
        for frame in range(60):
            star.clear()
            
            # 计算当前六芒星大小
            size = frame * 5
            pulse = math.sin(frame * 0.2) * 5  # 脉冲效果
            
            # 绘制六芒星
            star.goto(0, 0)
            star.pendown()
            
            # 第一个三角形
            for i in range(3):
                star.forward(size + pulse)
                star.left(120)
            
            # 第二个三角形
            star.right(60)
            for i in range(3):
                star.forward(size + pulse)
                star.right(120)
            
            star.penup()
            
            # 添加旋转效果
            if frame > 20:
                star.clear()
                star.goto(0, 0)
                star.pendown()
                
                # 旋转角度
                angle = frame * 3
                
                # 第一个旋转三角形
                star.setheading(30 + angle)
                for i in range(3):
                    star.forward(size + pulse)
                    star.left(120)
                
                # 第二个旋转三角形
                star.setheading(90 + angle)
                for i in range(3):
                    star.forward(size + pulse)
                    star.right(120)
                
                star.penup()
            
            # 添加666数字脉冲效果
            if frame > 10:
                center_text = turtle.Turtle()
                center_text.hideturtle()
                center_text.penup()
                center_text.color("#FF0000")
                center_text.goto(0, -10)
                
                # 数字666的脉冲效果
                text_size = 16 + math.sin(frame * 0.3) * 4
                center_text.write("666", align="center", 
                                font=("Arial", int(text_size), "bold"))
                
                self.screen.update()
                time.sleep(0.03)
                
                # 清除中心文字
                center_text.clear()
            else:
                self.screen.update()
                time.sleep(0.03)
        
        star.hideturtle()
        self.animation_complete = True
        
    def show_input_fields(self):
        """显示输入框"""
        # 清除之前的显示
        self.clear_input_display()
        
        # 标题
        title = turtle.Turtle()
        title.hideturtle()
        title.penup()
        title.color("white")
        title.goto(0, -150)
        title.write("LIFE VERIFICATION REQUIRED", align="center", 
                   font=("Arial", 18, "bold"))
        
        # 蓝色代码输入提示
        blue_prompt = turtle.Turtle()
        blue_prompt.hideturtle()
        blue_prompt.penup()
        blue_prompt.color("white")
        blue_prompt.goto(-200, -200)
        blue_prompt.write("Enter BLUE code:", align="left", 
                         font=("Arial", 14, "normal"))
        
        # 紫色代码输入提示
        purple_prompt = turtle.Turtle()
        purple_prompt.hideturtle()
        purple_prompt.penup()
        purple_prompt.color("white")
        purple_prompt.goto(-200, -230)
        purple_prompt.write("Enter PURPLE code:", align="left",
                           font=("Arial", 14, "normal"))
        
        # 显示当前输入状态
        self.update_input_display()
        
        # 操作提示
        hint = turtle.Turtle()
        hint.hideturtle()
        hint.penup()
        hint.color("yellow")
        hint.goto(0, -270)
        hint.write("TAB: Switch input | ENTER: Submit | BACKSPACE: Delete", 
                  align="center", font=("Arial", 12, "normal"))
        
    def clear_input_display(self):
        """清除输入显示"""
        for turtle_obj in self.screen.turtles():
            if hasattr(turtle_obj, 'is_input_display'):
                turtle_obj.clear()
                
    def update_input_display(self):
        """更新输入显示"""
        # 清除之前的输入显示
        self.clear_input_display()
        
        # 显示蓝色代码输入
        blue_display = turtle.Turtle()
        blue_display.hideturtle()
        blue_display.penup()
        blue_display.is_input_display = True
        
        if self.current_input == "blue":
            blue_display.color("cyan")  # 高亮当前输入框
        else:
            blue_display.color("white")
            
        blue_display.goto(50, -200)
        display_text = self.blue_code if self.blue_code else "____"
        blue_display.write(display_text, align="left", font=("Courier", 16, "bold"))
        
        # 显示紫色代码输入
        purple_display = turtle.Turtle()
        purple_display.hideturtle()
        purple_display.penup()
        purple_display.is_input_display = True
        
        if self.current_input == "purple":
            purple_display.color("magenta")  # 高亮当前输入框
        else:
            purple_display.color("white")
            
        purple_display.goto(50, -230)
        display_text = self.purple_code if self.purple_code else "____"
        purple_display.write(display_text, align="left", font=("Courier", 16, "bold"))
        
        # 如果两个代码都输入了，检查验证
        if len(self.blue_code) == 4 and len(self.purple_code) == 4:
            self.check_verification()
    
    def check_verification(self):
        """检查代码验证"""
        if self.blue_code.upper() == "ALEX" and self.purple_code.upper() == "TODD":
            self.verification_passed = True
            self.show_success_message()
        else:
            # 验证失败，清空输入
            self.blue_code = ""
            self.purple_code = ""
            self.current_input = "blue"
            self.show_error_message()
    
    def show_success_message(self):
        """显示验证成功消息"""
        success = turtle.Turtle()
        success.hideturtle()
        success.penup()
        success.color("#00FF00")
        success.goto(0, -300)
        success.write("✓ LIFE VERIFICATION SUCCESSFUL ✓", align="center", 
                     font=("Arial", 16, "bold"))
        
        # 2秒后进入下一个场景
        self.screen.ontimer(self.transition_to_snake, 2000)
    
    def show_error_message(self):
        """显示验证错误消息"""
        error = turtle.Turtle()
        error.hideturtle()
        error.penup()
        error.color("#FF0000")
        error.goto(0, -300)
        error.write("✗ VERIFICATION FAILED - TRY AGAIN ✗", align="center",
                   font=("Arial", 16, "bold"))
        
        # 1.5秒后清除错误消息并更新显示
        self.screen.ontimer(lambda: (error.clear(), self.update_input_display()), 1500)
    
    def process_keypress(self, key):
        """处理按键输入"""
        if not self.animation_complete or self.verification_passed:
            return
            
        if key.isalpha() and len(key) == 1:
            # 字母输入
            if self.current_input == "blue" and len(self.blue_code) < 4:
                self.blue_code += key.upper()
            elif self.current_input == "purple" and len(self.purple_code) < 4:
                self.purple_code += key.upper()
                
        elif key == "BackSpace":
            # 退格键
            if self.current_input == "blue" and self.blue_code:
                self.blue_code = self.blue_code[:-1]
            elif self.current_input == "purple" and self.purple_code:
                self.purple_code = self.purple_code[:-1]
                
        elif key == "Tab":
            # 切换输入框
            self.current_input = "purple" if self.current_input == "blue" else "blue"
            
        elif key == "Return":
            # 回车键提交
            if self.current_input == "blue" and len(self.blue_code) == 4:
                self.current_input = "purple"
            elif self.current_input == "purple" and len(self.purple_code) == 4:
                self.check_verification()
        
        self.update_input_display()
    
    def transition_to_snake(self):
        """过渡到贪吃蛇游戏介绍场景"""
        # 红色过渡效果
        transition = turtle.Turtle()
        transition.hideturtle()
        transition.penup()
        transition.color("#FF0000")
        transition.goto(0, 0)
        
        # 红色逐渐充满屏幕
        for size in range(0, 500, 15):
            transition.clear()
            transition.dot(size)
            self.screen.update()
            time.sleep(0.02)
        
        # 短暂显示红色屏幕
        time.sleep(0.5)
        
        # 切换到红色贪吃蛇介绍场景
        self.manager.change_state(GameState.RED_SNAKE_INTRO)
    
    def run(self):
        """运行验证场景"""
        self.clear_screen()
        
        # 第一步：显示魔鬼头
        self.draw_demon_head()
        time.sleep(1)
        
        # 第二步：六芒星动画
        self.animate_hexagram_emergence()
        
        # 第三步：显示输入框
        self.show_input_fields()
        
        # 绑定按键
        self.screen.listen()
        
        # 绑定字母键
        for char in "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz":
            self.screen.onkeypress(lambda ch=char: self.process_keypress(ch), char)
        
        # 绑定功能键
        self.screen.onkeypress(lambda: self.process_keypress("BackSpace"), "BackSpace")
        self.screen.onkeypress(lambda: self.process_keypress("Tab"), "Tab")
        self.screen.onkeypress(lambda: self.process_keypress("Return"), "Return")
        
        # 主循环
        while self.manager.current_state == GameState.RED_STAR_VERIFICATION:
            self.screen.update()
            time.sleep(0.1)