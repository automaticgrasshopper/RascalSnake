import turtle
import time
from scenes.base_scene import BaseScene
from constants import GameState
from save_manager import SaveManager

class TrueEnding(BaseScene):
    def __init__(self, game_manager):
        super().__init__(game_manager)
        
    def run(self):
        """真结局演出"""
        self.clear_screen()
        
        # 显示真结局信息
        title = turtle.Turtle()
        title.hideturtle()
        title.penup()
        title.color("gold")
        title.goto(0, 100)
        title.write("TRUE ENDING UNLOCKED", align="center", font=("Arial", 24, "bold"))
        
        message = turtle.Turtle()
        message.hideturtle()
        message.penup()
        message.color("white")
        message.goto(0, 0)
        message.write("You have uncovered the ultimate truth", align="center", font=("Arial", 16, "normal"))
        
        # 这里可以添加更复杂的真结局演出
        
        continue_prompt = turtle.Turtle()
        continue_prompt.hideturtle()
        continue_prompt.penup()
        continue_prompt.color("yellow")
        continue_prompt.goto(0, -100)
        continue_prompt.write("Press SPACE to return to title", align="center", font=("Arial", 14, "normal"))
        
        self.screen.update()
        
        # 绑定按键
        self.screen.listen()
        self.screen.onkeypress(self.return_to_title, "space")
        
        # 等待
        while self.manager.current_state == GameState.TRUE_ENDING:
            self.screen.update()
            time.sleep(0.1)
            
    def return_to_title(self):
        """返回标题"""
        self.manager.change_state(GameState.TITLE)