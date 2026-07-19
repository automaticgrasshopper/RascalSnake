import turtle
import time
from scenes.base_scene import BaseScene
from constants import GameState
from save_manager import SaveManager

class PurpleEnding(BaseScene):
    def run(self):
        self.clear_screen()
        
        # 设置R键重新开始
        self.screen.listen()
        self.screen.onkeypress(self.restart_to_title, "r")
        self.screen.onkeypress(self.restart_to_title, "R")
        
        # 显示紫色墓碑ASCII艺术
        tombstone = turtle.Turtle()
        tombstone.hideturtle()
        tombstone.penup()
        tombstone.color("#8A2BE2")  # 紫色
        tombstone.goto(0, 0)
        
        tombstone_art = [
            "  _____________",
            " |             |",
            " |   REST IN   |", 
            " |    PEACE    |",
            " |             |",
            " |     Mike    |",
            " |  1999-2098  |",
            " |_____________|",
            "      |   |",
            "      |   |",
            "     _|___|_"
        ]
        
        for i, line in enumerate(tombstone_art):
            tombstone.goto(-90, 100 - i * 20)
            tombstone.write(line, align="left", font=("Courier", 12, "normal"))
            
        # 墓碑上的文字 - 紫色
        epitaph = turtle.Turtle()
        epitaph.hideturtle()
        epitaph.penup()
        epitaph.color("#8A2BE2")  # 紫色
        epitaph.goto(0, -150)
        epitaph.write("Hardworking and honest Mike buried here", 
                     align="center", font=("Arial", 14, "normal"))
        
        # 新增CODE-TODD文字 - 紫色
        code_todd = turtle.Turtle()
        code_todd.hideturtle()
        code_todd.penup()
        code_todd.color("#8A2BE2")  # 紫色
        code_todd.goto(0, -180)
        code_todd.write("CODE-TODD", align="center", font=("Arial", 14, "bold"))
        
        # 重新开始提示
        restart_prompt = turtle.Turtle()
        restart_prompt.hideturtle()
        restart_prompt.penup()
        restart_prompt.color("yellow")
        restart_prompt.goto(0, -220)
        restart_prompt.write("Press R to return to title", align="center", font=("Arial", 12, "normal"))
        
        # 在显示墓碑时保存游戏状态
        self.manager.save_data.purple_completed = True
        # 更新历史总分
        if self.manager.session_total_score > self.manager.save_data.historical_total:
            self.manager.save_data.historical_total = self.manager.session_total_score
        SaveManager.save_game(self.manager.save_data)
        
        self.manager.score_display.update()
        self.screen.update()
        
        # 等待玩家操作
        while self.manager.current_state == GameState.PURPLE_ENDING:
            self.screen.update()
            time.sleep(0.1)
            
    def restart_to_title(self):
        """重新开始游戏"""
        self.manager.restart_to_title()