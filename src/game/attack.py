import pygame
from src.utils.settings import *


class Attack(pygame.sprite.Sprite):
    def __init__(self, player, groups, z=LAYERS['main']):

        # general setup
        super().__init__(groups)
        self.sprite_type = 'attack'
        self.direction = player.status.split('_')[0]
        self.z = z

        self.image = pygame.Surface((15, 15))
        self.right_attack_image = pygame.Surface((30, 20))
        self.left_attack_image = pygame.Surface((30, 20))
        self.up_attack_image = pygame.Surface((30, 20))
        self.down_attack_image = pygame.Surface((30, 20))

        # placement
        if self.direction == 'right':
            self.image = self.right_attack_image
            self.rect = self.image.get_rect(midleft=player.hitbox.midright + pygame.math.Vector2(-20, 16))
        elif self.direction == 'left':
            self.image = self.left_attack_image
            self.rect = self.image.get_rect(midright=player.hitbox.midleft + pygame.math.Vector2(10, 16))
        elif self.direction == 'down':
            self.image = self.down_attack_image
            self.rect = self.image.get_rect(midtop=player.hitbox.midbottom + pygame.math.Vector2(0, 0))
        else:
            self.image = self.up_attack_image
            self.rect = self.image.get_rect(midbottom=player.hitbox.midtop + pygame.math.Vector2(0, 20))

