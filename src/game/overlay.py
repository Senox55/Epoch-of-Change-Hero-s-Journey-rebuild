import pygame
from src.utils.settings import *


class Overlay:
    def __init__(self, player):
        # general setup
        self.display_surface = pygame.display.get_surface()
        self.player = player

        # bar setop
        self.health_bar_rect = pygame.Rect(10, 10, HEALTH_BAR_WIDTH, HEALTH_BAR_HEIGHT)

        # imports
        overlay_path = r'..\Epoch-of-Change-Hero-s-Journey-rebuild\assets\overlay/'
        self.tools_surf = {tool: pygame.image.load(f'{overlay_path}{tool}.png').convert_alpha() for tool in
                           player.tools}

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

    def selection_box(self, position):
        bg_rect = pygame.Rect(position, (ITEM_BOX_SIZE, ITEM_BOX_SIZE))
        pygame.draw.rect(self.display_surface, OVERLAY_BG_COLOR, bg_rect)
        pygame.draw.rect(self.display_surface, OVERLAY_BORDER_COLOR, bg_rect, 3)

    def display(self):
        # bars
        self.show_bar(self.player.health, self.player.stats['health'], self.health_bar_rect, HEALTH_COLOR)
        self.selection_box((32, SCREEN_HEIGHT - ITEM_BOX_SIZE - 7))

        # tools
        tool_surf = self.tools_surf[self.player.selected_tool]
        tool_rect = tool_surf.get_rect(bottomleft=OVERLAY_POSITIONS['tool'])
        self.display_surface.blit(tool_surf, tool_rect)
