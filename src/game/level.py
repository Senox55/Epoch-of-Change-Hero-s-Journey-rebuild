import pygame
from src.utils.settings import *
from src.game.player import Player
from src.game.overlay import Overlay
from src.utils.sprites import Generic
from pytmx.util_pygame import load_pygame


class Level:
    def __init__(self):
        # get the display surface
        self.display_surface = pygame.display.get_surface()

        # sprite groups
        self.all_sprites = CameraGroup()

        self.setup()
        self.overlay = Overlay(self.player)

    def setup(self):


        self.player = Player((640, 360), group=self.all_sprites)

        Generic(pos=(0, 0), surf=pygame.image.load(
            r'..\Epoch-of-Change-Hero-s-Journey-rebuild\assets\world\ground.png').convert_alpha(),
                groups=self.all_sprites, z=LAYERS['ground'])

    def run(self, dt):
        self.display_surface.fill('black')
        # self.all_sprites.draw(self.display_surface)
        self.all_sprites.custom_draw(self.player)
        self.all_sprites.update(dt)

        self.overlay.display()


class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.current_size = self.display_surface.get_size()

        # camera offset
        self.offset = pygame.math.Vector2()
        self.virtual_surface = pygame.Surface((VIRTUAL_SCREEN_WIDTH, VIRTUAL_SCREEN_HEIGHT))

    def center_target_camera(self, target):
        self.offset.x = target.rect.centerx - (VIRTUAL_SCREEN_WIDTH // 2)
        self.offset.y = target.rect.centery - (VIRTUAL_SCREEN_HEIGHT // 2)

    def custom_draw(self, player):
        self.center_target_camera(player)

        for layer in LAYERS.values():
            for sprite in self.sprites():
                if sprite.z == layer:
                    offset_rect = sprite.rect.copy()
                    offset_rect.center -= self.offset
                    self.virtual_surface.blit(sprite.image, offset_rect)
        scaled_surf = pygame.transform.scale(self.virtual_surface, self.current_size)
        self.display_surface.blit(scaled_surf, (0, 0))
