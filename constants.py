from enum import Enum

class GameState(Enum):
    TITLE = 1
    SNAKE_GAME = 2
    PURPLE_ENDING = 3
    BLUE_MODE = 4
    BLUE_BREAKOUT = 5
    BLUE_PLANE = 6
    BLUE_QTE = 7
    RED_ENDING = 8
    RED_STAR_VERIFICATION = 9
    RED_SNAKE_INTRO = 10
    RED_SNAKE = 11
    RED_BREAKOUT_INTRO = 12
    RED_BREAKOUT = 13
    RED_PLANE_INTRO = 14
    RED_PLANE = 15
    RED_QTE_INTRO = 16
    RED_QTE = 17
    RED_FINAL_VERIFICATION = 18
    TRUE_ENDING = 19
    NORMAL_SNAKE = 20
    RED_BREAKOUT_SNAKE = 21  # 新增：红色打砖块蛇模式

# 其他常量保持不变...
# 新增：红色打砖块蛇模式参数
RED_SNAKE_FOOD_POINTS = 666  # 蛇模式吃到食物的奖励分数

# 屏幕设置
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BG_COLOR = "black"

# 颜色定义
WALL_COLOR = "#808080"
SNAKE_HEAD_COLOR = "#6A0DAD"
SNAKE_BODY_COLORS = [
    "#7B1FA2",
    "#8E24AA", 
    "#9C27B0",
    "#AB47BC",
    "#BA68C8",
]
FOOD_COLOR = "#8A2BE2"

# 游戏参数
SNAKE_SPEED = 0.1
FOOD_POINTS = 37
PURPLE_ENDING_SCORE = 999
SPECIAL_FOOD_SPAWN_SCORE = 666

# 蓝色模式参数
BLUE_BLOCK_POINTS = 40
PADDLE_SHRINK_SCORE = 200
MIN_PADDLE_WIDTH = 20

# 飞机游戏参数
PLANE_ENEMY_POINTS = 150
PLANE_ENEMY_COUNT = 6
PLANE_MESSAGES = [
    "This is not your fault",
    "This is a necessary mission",
    "Help me",
    "Don't listen to unnecessary voices", 
    "Kill them and you'll be happy, Sergeant",
    "They are monsters"
]

# QTE游戏参数
QTE_KEYS = ["A", "S", "D", "F", "J", "K", "L"]
QTE_SEQUENCE_LENGTH = 6
QTE_MAX_TIMER = 90
QTE_TOTAL_ROUNDS = 3
QTE_MONSTER_HEALTH = 15

# 红色模式参数
RED_PLANE_TARGET = 6
RED_QTE_TARGET = 1000
RED_FINAL_SCORE_REQUIRED = 10000
RED_CODE = "MIKE"

# 新增：普通贪吃蛇参数
NORMAL_SNAKE_VICTORY_SCORE = 6666

# 新增：红色打砖块参数
RED_BLOCK_POINTS = 40  # 红色砖块分数
RED_SNAKE_FOOD_POINTS = 666  # 蛇模式吃到食物的奖励分数
RED_SNAKE_PADDLE_LENGTH = 5  # 蛇挡板的初始长度
RED_SNAKE_SPEED = 3  # 蛇模式移动速度（帧数控制）