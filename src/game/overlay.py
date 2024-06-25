import pygame
from src.utils.settings import *


class Overlay:
    def __init__(self, player):
        # general setup
        self.display_surface = pygame.display.get_surface()
        self.player = player
        self.font = pygame.font.Font(None, EXP_TEXT_SIZE)

        # bar setop
        self.health_bar_rect = pygame.Rect(10, 10, HEALTH_BAR_WIDTH, HEALTH_BAR_HEIGHT)
        self.energy_bar_rect = pygame.Rect(10, 35, ENERGY_BAR_WIDTH, ENERGY_BAR_HEIGHT)

        # imports
        overlay_path = r'..\Epoch-of-Change-Hero-s-Journey-rebuild\assets\overlay/'
        self.weapons_surf = {tool: pygame.image.load(f'{overlay_path}{tool}.png').convert_alpha() for tool in
                             player.weapons}

        self.magics_surf = {magic: pygame.image.load(f'{overlay_path}{magic}.png').convert_alpha() for magic in
                            player.magics}

    def show_bar(self, current, max_amount, bg_rect, colour):
        # draw bg
        pygame.draw.rect(self.display_surface, BLACK, bg_rect)

        # converting stat to pixel
        ratio = current / max_amount
        current_width = bg_rect.width * ratio
        current_rect = bg_rect.copy()
        current_rect.width = current_width

        # drawing the bar
        pygame.draw.rect(self.display_surface, colour, current_rect)
        pygame.draw.rect(self.display_surface, OVERLAY_BORDER_COLOR, bg_rect, 4)

    def selection_box(self, position, width, height):
        bg_rect = pygame.Rect(position, (width, height))
        pygame.draw.rect(self.display_surface, OVERLAY_BG_COLOR, bg_rect)
        pygame.draw.rect(self.display_surface, OVERLAY_BORDER_COLOR, bg_rect, 3)

    def show_exp(self, exp):
        text_surf = self.font.render(str(int(exp)), True, TEXT_COLOR)
        x = self.display_surface.get_size()[0] - 20
        y = self.display_surface.get_size()[1] - 15
        text_rect = text_surf.get_rect(bottomright=(x,y))

        self.display_surface.blit(text_surf, text_rect)

    def display(self):
        # bars
        self.show_bar(self.player.health, self.player.stats['health'], self.health_bar_rect, HEALTH_COLOR)
        self.show_bar(self.player.energy, self.player.stats['energy'], self.energy_bar_rect, ENERGY_COLOR)
        self.selection_box((32, SCREEN_HEIGHT - ITEM_BOX_SIZE - 7), ITEM_BOX_SIZE, ITEM_BOX_SIZE)
        self.selection_box((100, SCREEN_HEIGHT - MAGIC_BOX_SIZE - 3), MAGIC_BOX_SIZE, MAGIC_BOX_SIZE)
        self.selection_box((SCREEN_WIDTH - EXP_BOX_WIDTH - 10, SCREEN_HEIGHT - EXP_BOX_HEIGHT - 10), EXP_BOX_WIDTH,
                           EXP_BOX_HEIGHT)

        self.show_exp(self.player.exp)

        # weapons
        weapon_surf = self.weapons_surf[self.player.weapon]
        weapon_rect = weapon_surf.get_rect(bottomleft=OVERLAY_POSITIONS['tool'])
        self.display_surface.blit(weapon_surf, weapon_rect)

        # magics
        magic_surf = self.magics_surf[self.player.magic]
        magic_rect = magic_surf.get_rect(bottomleft=OVERLAY_POSITIONS['magic'])
        self.display_surface.blit(magic_surf, magic_rect)
