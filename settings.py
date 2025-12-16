import pygame


WIDTH, HEIGHT = 800, 600
UI_HEIGHT = 100
MAP_HEIGHT = HEIGHT - UI_HEIGHT
FPS = 60


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 50, 50)
GREEN = (50, 200, 50)
BLUE = (50, 50, 200)
YELLOW = (200, 200, 50)
GRAY = (100, 100, 100)
BROWN = (139, 69, 19)
PATH_COLOR = (200, 180, 130)

STARTING_MONEY = 250
STARTING_LIVES = 10
WIN_WAVE = 5


PATH_POINTS = [
    (-50, 100), (700, 100), (700, 500), (100, 500),
    (100, 200), (600, 200), (600, 400), (200, 400),
    (200, 300), (400, 300) 
]
BASE_POS = PATH_POINTS[-1]


TOWER_TYPES = {
    "Archer": {"cost": 50, "range": 120, "damage": 10, "cooldown": 800, "color": GREEN, "name": "Archer"},
    "Mage":   {"cost": 100, "range": 80,  "damage": 30, "cooldown": 1500, "color": BLUE, "name": "Mage"},
    "Sniper": {"cost": 150, "range": 200, "damage": 50, "cooldown": 2500, "color": YELLOW, "name": "Sniper"}
}


WAVES = [
    {"count": 5, "hp": 30, "spd": 2, "rew": 15, "delay": 1000, "grade": 0},
    {"count": 8, "hp": 40, "spd": 2.5, "rew": 15, "delay": 800, "grade": 1},
    {"count": 4, "hp": 120, "spd": 1.5, "rew": 30, "delay": 1500, "grade": 2},
    {"count": 15, "hp": 30, "spd": 4, "rew": 10, "delay": 400, "grade": 1},
    {"count": 10, "hp": 150, "spd": 2, "rew": 25, "delay": 1000, "grade": 3},
]