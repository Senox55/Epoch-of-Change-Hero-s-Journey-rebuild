import pygame
from src.utils.settings import *


class Attack(pygame.sprite.Sprite):
    def __init__(self, player, groups, z=LAYERS['main']):

        # general setup
        super().__init__(groups)
        self.sprite_type = 'attack'
        self.direction = player.status.split('_')[0]
        self.z = z

        self.images = {
            'right': pygame.Surface((25, 15)),
            'left': pygame.Surface((25, 15)),
            'up': pygame.Surface((15, 23)),
            'down': pygame.Surface((15, 23))
        }

        self.image = self.images[self.direction]


        # placement
        if self.direction == 'right':
            self.rect = self.image.get_rect(midleft=player.hitbox.midright + pygame.math.Vector2(0, 14))
        elif self.direction == 'left':
            self.rect = self.image.get_rect(midright=player.hitbox.midleft + pygame.math.Vector2(30, 14))
        elif self.direction == 'down':
            self.rect = self.image.get_rect(midtop=player.hitbox.midbottom + pygame.math.Vector2(0, -20))
        else:
            self.rect = self.image.get_rect(midbottom=player.hitbox.midtop + pygame.math.Vector2(0, 40))

