import pygame

# screen
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
VIRTUAL_SCREEN_WIDTH = SCREEN_WIDTH // 2
VIRTUAL_SCREEN_HEIGHT = SCREEN_HEIGHT // 2

TILESIZE = 32

# overlay
HEALTH_BAR_WIDTH = 200
HEALTH_BAR_HEIGHT = 20
ITEM_BOX_SIZE = 80
OVERLAY_POSITIONS = {
    'tool': (40, SCREEN_HEIGHT - 15)
}

# layers
LAYERS = {
    'ground': 0,
    'main': 1
}

# general colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREY = (128, 128, 128)
GREEN = (0, 255, 0)
GREY_GREEN = (23, 114, 69)
DARK_GREY = (96, 96, 96)
LIGHT_BLUE = (175, 238, 238)
GREY_BLUE = (81, 183, 183)

# overlay colors
HEALTH_COLOR = 'red'
OVERLAY_BORDER_COLOR = BLACK
OVERLAY_BG_COLOR = DARK_GREY

# time
SECOND_TO_MILLISECOND = 1000

# enemy
monster_data = {
    'slime': {'health': 100, 'damage': 10, 'speed': 30, 'attack_radius': 1, 'notice_radius': 400, 'repulsion': 1,
              'attack_type': 'splash', 'hitbox': {'x': 8, 'y': 13, 'width': 16, 'height': 10}},
    'giant_slime': {'health': 1000, 'damage': 30, 'speed': 50, 'attack_radius': 100, 'notice_radius': 400,
                    'repulsion': 1,
                    'attack_type': 'splash', 'hitbox': {'x': 80, 'y': 130, 'width': 160, 'height': 100}}
}

# attack attributes
TIME_ATTACKING = 350

# menu
START_BUTTON_WIDTH = 200
START_BUTTON_HEIGHT = 100
MENU_POSITIONS = {
    'start': (SCREEN_WIDTH // 2 - 300, SCREEN_HEIGHT // 2),
    'exit': (SCREEN_WIDTH // 2 + 300, SCREEN_HEIGHT // 2),
    'restart': (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 200),
    'win': (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 300),
    'restart_after_win': (SCREEN_WIDTH // 2 - 300, SCREEN_HEIGHT // 2)
}
