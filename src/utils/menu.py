import pygame
from src.utils.settings import *
from src.utils.support import *
from src.utils.button import Button


class Menu:
    def __init__(self):
        self.import_assets()
        self.buttons = [Button('start', MENU_POSITIONS['start'], self.buttons_images['start']),
                        Button('exit', MENU_POSITIONS['exit'], self.buttons_images['exit'])]

    def import_assets(self):
        self.buttons_images = {'start': None, 'exit': None}

        for button_image in self.buttons_images.keys():
            full_path = r'..\Epoch-of-Change-Hero-s-Journey-rebuild\assets\menu\buttons/' + button_image + '.png'
            self.buttons_images[button_image] = pygame.image.load(full_path).convert_alpha()

    def draw(self, screen):
        screen.fill(BLACK)
        for button in self.buttons:
            button.draw(screen)

    def check_clicked_button(self):
        for button in self.buttons:
            if button.clicked:
                return button.name
