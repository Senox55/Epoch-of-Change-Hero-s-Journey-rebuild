import pygame
from src.utils.settings import *


class Text(pygame.sprite.Sprite):
    def __init__(self, pos, size, text, colour, groups, z=LAYERS['text']):
        super().__init__(groups)
        self.size = size
        self.z = z
        self.font = pygame.font.Font(None, self.size)
        self.image = self.font.render(text, True, colour)
        self.rect = self.image.get_rect(center=pos)

    def display(self, screen):
        screen.blit(self.image, self.rect)
