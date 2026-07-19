import turtle

class BaseScene:
    def __init__(self, game_manager):
        self.manager = game_manager
        self.screen = game_manager.screen
        
    def clear_screen(self):
        """清除屏幕"""
        for turtle_obj in self.screen.turtles():
            if hasattr(self.manager, 'score_display') and turtle_obj in self.manager.score_display.turtles:
                continue
            turtle_obj.clear()
            turtle_obj.hideturtle()
                
    def run(self):
        """运行场景"""
        raise NotImplementedError("子类必须实现run()方法")