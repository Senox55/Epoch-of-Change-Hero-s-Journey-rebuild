import random

import pygame
from src.utils.settings import *


class MagicPlayer:
    def __init__(self, animation_player):
        self.animation_player = animation_player
        self.sounds = {
            'flame': pygame.mixer.Sound(r'..\Epoch-of-Change-Hero-s-Journey-rebuild\audio\attack\fire.mp3'),
            'heal': pygame.mixer.Sound(r'..\Epoch-of-Change-Hero-s-Journey-rebuild\audio\heal\heal.wav')
        }

    def heal(self, player, strength, cost, groups):
        if player.energy >= 0:
            self.sounds['heal'].play()
            player.health += strength
            player.energy -= cost
            if player.health >= player.stats['health']:
                player.health = player.stats['health']
            self.animation_player.create_particles('heal', player.rect.center + pygame.math.Vector2(0, 5), groups)

    def flame(self, player, cost, groups):
        if player.energy >= 0:
            self.sounds['flame'].play()
            player.energy -= cost

            if player.status.split('_')[0] == 'right':
                direction = pygame.math.Vector2(1, 0)
            elif player.status.split('_')[0] == 'left':
                direction = pygame.math.Vector2(-1, 0)
            elif player.status.split('_')[0] == 'up':
                direction = pygame.math.Vector2(0, -1)
            else:
                direction = pygame.math.Vector2(0, 1)

            for i in range(1, 6):
                if direction.x:  # horizontal
                    offset_x = (direction.x * i) * TILESIZE
                    x = player.rect.centerx + offset_x + random.randint(-TILESIZE // 3, TILESIZE // 3)
                    y = player.rect.centery + random.randint(-TILESIZE // 3, TILESIZE // 3)
                    self.animation_player.create_particles('flame', (x, y), groups)
                else:  # vertical
                    offset_y = (direction.y * i) * TILESIZE
                    x = player.rect.centerx + random.randint(-TILESIZE // 3, TILESIZE // 3)
                    y = player.rect.centery + offset_y + random.randint(-TILESIZE // 3, TILESIZE // 3)
                    self.animation_player.create_particles('flame', (x, y), groups)
