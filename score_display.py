import turtle
import time

class ScoreDisplay:
    def __init__(self, game_manager):
        self.manager = game_manager
        self.turtles = []
        self.create_display()
        
    def create_display(self):
        # 当前游戏分数
        self.current_score_turtle = turtle.Turtle()
        self.current_score_turtle.hideturtle()
        self.current_score_turtle.penup()
        self.current_score_turtle.color("white")
        self.current_score_turtle.goto(-380, 250)
        self.turtles.append(self.current_score_turtle)
        
        # 总分
        total_score = turtle.Turtle()
        total_score.hideturtle()
        total_score.penup()
        total_score.color("white")
        total_score.goto(-380, 220)
        self.turtles.append(total_score)
        
        # 历史总分
        historical_total = turtle.Turtle()
        historical_total.hideturtle()
        historical_total.penup()
        historical_total.color("white")
        historical_total.goto(-380, 190)
        self.turtles.append(historical_total)
        
        self.update()
        
    def update(self):
        # 当前游戏分数
        score_color = "red" if self.manager.current_game_score == 666 else "white"
        self.current_score_turtle.color(score_color)
        self.current_score_turtle.clear()
        self.current_score_turtle.write(f"Score: {self.manager.current_game_score}", 
                                       align="left", font=("Arial", 12, "normal"))
        
        # 总分
        self.turtles[1].clear()
        self.turtles[1].write(f"Total: {self.manager.session_total_score}", 
                             align="left", font=("Arial", 12, "normal"))
        
        # 历史总分
        self.turtles[2].clear()
        self.turtles[2].write(f"Historical: {self.manager.save_data.historical_total}", 
                             align="left", font=("Arial", 12, "normal"))