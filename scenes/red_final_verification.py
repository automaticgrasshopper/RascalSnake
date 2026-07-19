import turtle
import time
from scenes.base_scene import BaseScene
from constants import GameState, RED_FINAL_SCORE_REQUIRED, RED_CODE

class RedFinalVerification(BaseScene):
    def __init__(self, game_manager):
        super().__init__(game_manager)
        self.input_code = ""
        
    def run(self):
        """红色最终验证场景"""
        self.clear_screen()
        
        # 检查是否满足条件
        if not self.manager.check_red_final_unlock():
            self.show_locked_message()
            return
            
        self.show_verification_screen()
        
    def show_locked_message(self):
        """显示未解锁消息"""
        locked = turtle.Turtle()
        locked.hideturtle()
        locked.penup()
        locked.color("red")
        locked.goto(0, 100)
        locked.write("FINAL VERIFICATION LOCKED", align="center", font=("Arial", 24, "bold"))
        
        requirements = turtle.Turtle()
        requirements.hideturtle()
        requirements.penup()
        requirements.color("white")
        requirements.goto(0, 0)
        requirements.write("Requirements:", align="center", font=("Arial", 16, "normal"))
        
        req_details = turtle.Turtle()
        req_details.hideturtle()
        req_details.penup()
        req_details.color("yellow")
        req_details.goto(0, -50)
        req_details.write(f"- Complete all three color routes\n- Fill the red form\n- Accumulate {RED_FINAL_SCORE_REQUIRED} total points", 
                         align="center", font=("Arial", 14, "normal"))
        
        current_score = turtle.Turtle()
        current_score.hideturtle()
        current_score.penup()
        current_score.color("cyan")
        current_score.goto(0, -150)
        current_score.write(f"Current Total: {self.manager.session_total_score}/{RED_FINAL_SCORE_REQUIRED}", 
                           align="center", font=("Arial", 14, "normal"))
        
        back_prompt = turtle.Turtle()
        back_prompt.hideturtle()
        back_prompt.penup()
        back_prompt.color("white")
        back_prompt.goto(0, -250)
        back_prompt.write("Press R to return to title", align="center", font=("Arial", 14, "normal"))
        
        self.screen.update()
        
        # 绑定按键
        self.screen.listen()
        self.screen.onkeypress(self.return_to_title, "r")
        self.screen.onkeypress(self.return_to_title, "R")
        
        # 等待
        while self.manager.current_state == GameState.RED_FINAL_VERIFICATION:
            self.screen.update()
            time.sleep(0.1)
            
    def show_verification_screen(self):
        """显示验证屏幕"""
        title = turtle.Turtle()
        title.hideturtle()
        title.penup()
        title.color("red")
        title.goto(0, 100)
        title.write("FINAL VERIFICATION", align="center", font=("Arial", 24, "bold"))
        
        prompt = turtle.Turtle()
        prompt.hideturtle()
        prompt.penup()
        prompt.color("white")
        prompt.goto(0, 0)
        prompt.write("Enter the RED code:", align="center", font=("Arial", 16, "normal"))
        
        # 显示输入框
        self.update_input_display()
        
        # 绑定按键
        self.screen.listen()
        for char in "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz":
            self.screen.onkeypress(lambda ch=char: self.process_keypress(ch), char)
        self.screen.onkeypress(lambda: self.process_keypress("BackSpace"), "BackSpace")
        self.screen.onkeypress(self.submit_code, "Return")
        
        # 等待输入
        while self.manager.current_state == GameState.RED_FINAL_VERIFICATION:
            self.screen.update()
            time.sleep(0.1)
            
    def update_input_display(self):
        """更新输入显示"""
        # 清除之前的显示
        for turtle_obj in self.screen.turtles():
            if hasattr(turtle_obj, 'is_code_display'):
                turtle_obj.clear()
                
        # 显示当前输入
        code_display = turtle.Turtle()
        code_display.hideturtle()
        code_display.penup()
        code_display.is_code_display = True
        code_display.color("red")
        code_display.goto(0, -50)
        display_text = self.input_code if self.input_code else "_____"
        code_display.write(display_text, align="center", font=("Courier", 20, "bold"))
        
    def process_keypress(self, key):
        """处理按键"""
        if key == "BackSpace":
            if self.input_code:
                self.input_code = self.input_code[:-1]
        elif key.isalpha() and len(key) == 1:
            if len(self.input_code) < 5:  # 限制为5个字符
                self.input_code += key.upper()
                
        self.update_input_display()
        
    def submit_code(self):
        """提交代码验证"""
        if self.input_code.upper() == RED_CODE:
            self.verification_success()
        else:
            self.verification_failed()
            
    def verification_success(self):
        """验证成功"""
        success = turtle.Turtle()
        success.hideturtle()
        success.penup()
        success.color("#00FF00")
        success.goto(0, -100)
        success.write("✓ VERIFICATION SUCCESSFUL ✓", align="center", font=("Arial", 18, "bold"))
        
        # 设置红色表单完成标志
        self.manager.save_data.red_form_completed = True
        from save_manager import SaveManager
        SaveManager.save_game(self.manager.save_data)
        
        self.screen.update()
        time.sleep(2)
        
        # 进入真结局
        self.manager.change_state(GameState.TRUE_ENDING)
        
    def verification_failed(self):
        """验证失败"""
        error = turtle.Turtle()
        error.hideturtle()
        error.penup()
        error.color("#FF0000")
        error.goto(0, -100)
        error.write("✗ VERIFICATION FAILED ✗", align="center", font=("Arial", 18, "bold"))
        
        self.input_code = ""
        self.update_input_display()
        
        self.screen.update()
        time.sleep(1.5)
        
    def return_to_title(self):
        """返回标题"""
        self.manager.change_state(GameState.TITLE)