import pygame
from src.utils.settings import *


class MagicPlayer:
    def __init__(self, animation_player):
        self.animation_player = animation_player

    def heal(self, player, strength, cost, groups):
        if player.energy > 0:
            player.health += strength
            player.energy -= cost
            if player.health >= player.stats['health']:
                player.health = player.stats['health']
                self.animation_player.create_particles('heal', player.rect.center, groups)

    def flame(self):
        pass
