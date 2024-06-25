import pygame
from src.utils.settings import *


class Generic(pygame.sprite.Sprite):
    def __init__(self, pos, surf, sprite_type, groups, z=LAYERS['main']):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft=pos)
        self.z = z
        self.sprite_type = sprite_type
        self.hitbox = self.rect.copy()


class Tree(Generic):
    def __init__(self, pos, surf, sprite_type, groups):
        super().__init__(pos, surf, sprite_type, groups)
        self.hitbox = self.rect.copy().inflate(-20, -20)


class Bush(Generic):
    def __init__(self, pos, surf, sprite_type, groups):
        super().__init__(pos, surf, sprite_type, groups)
        self.hitbox = self.rect.copy().inflate(-30, -30)


class Coffin(Generic):
    def __init__(self, pos, surf, sprite_type, groups):
        super().__init__(pos, surf, sprite_type, groups)
        self.hitbox = self.rect.copy().inflate(-10, -10)


class Finish(Generic):
    def __init__(self, pos, surf, sprite_type, groups):
        super().__init__(pos, surf, sprite_type, groups)
