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
ENERGY_BAR_WIDTH = 100
ENERGY_BAR_HEIGHT = 20
ITEM_BOX_SIZE = 80
MAGIC_BOX_SIZE = 80
EXP_BOX_WIDTH = 80
EXP_BOX_HEIGHT = 30
EXP_TEXT_SIZE = 30
OVERLAY_POSITIONS = {
    'tool': (40, SCREEN_HEIGHT - 15),
    'magic': (108, SCREEN_HEIGHT - 11)
}

# layers
LAYERS = {
    'ground': 0,
    'main': 1,
    'text': 2,
}

# general colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREY = (128, 128, 128)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GREY_GREEN = (23, 114, 69)
DARK_GREY = (96, 96, 96)
LIGHT_BLUE = (175, 238, 238)
GREY_BLUE = (81, 183, 183)

# overlay colors
HEALTH_COLOR = RED
TEXT_COLOR = BLACK
ENERGY_COLOR = BLUE
OVERLAY_BORDER_COLOR = BLACK
OVERLAY_BG_COLOR = DARK_GREY

# time
SECOND_TO_MILLISECOND = 1000

# enemy
monster_data = {
    'slime': {'health': 100, 'damage': 10, 'speed': 30, 'attack_radius': 1, 'notice_radius': 400, 'repulsion': 1,
              'attack_type': 'splash', 'hitbox': {'x': 8, 'y': 13, 'width': 16, 'height': 10}, 'exp': 10},
    'giant_slime': {'health': 700, 'damage': 20, 'speed': 60, 'attack_radius': 100, 'notice_radius': 1500,
                    'repulsion': 1,
                    'attack_type': 'splash', 'hitbox': {'x': 80, 'y': 130, 'width': 160, 'height': 100}, 'exp': 100}
}

# attack attributes
TIME_ATTACKING = 350

# magic attributes
TIME_HEALING = 600

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

# weapons
weapons_data = {'katana': {'damage': 30, 'attack_type': 'splash'},
                'simple_sword': {'damage': 15, 'attack_type': 'splash'}
                }

# magics
magics_data = {'heal': {'style': 'heal', 'strength': 40, 'cost': 10},
               'flame': {'style': 'flame', 'strength': 40, 'cost': 10},
               }

# texts
TEXTS_POSITIONS = {
    'warn_about_exp': (SCREEN_WIDTH // 2 + 300, SCREEN_HEIGHT // 2 - 300)
}
