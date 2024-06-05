import pygame
from src.utils.settings import *
from src.game.player import Player
from src.game.overlay import Overlay
from src.utils.sprites import Generic, Tree, Bush
from pytmx.util_pygame import load_pygame


class Level:
    def __init__(self):
        # get the display surface
        self.display_surface = pygame.display.get_surface()

        # sprite groups
        self.all_sprites = CameraGroup()
        self.collision_sprites = pygame.sprite.Group()

        self.setup()
        self.overlay = Overlay(self.player)

    def setup(self):
        tmx_data = load_pygame(r'..\Epoch-of-Change-Hero-s-Journey-rebuild\data\map.tmx')

        # ground
        for x, y, surf in tmx_data.get_layer_by_name('ground').tiles():
            pos = (x * TILESIZE, y * TILESIZE)
            Generic(pos, surf, self.all_sprites, LAYERS['ground'])

        # bushes
        for obj in tmx_data.get_layer_by_name('bushes'):
            pos = (obj.x, obj.y)
            Bush(pos, obj.image, groups=[self.all_sprites, self.collision_sprites])

        self.player = Player((500, 500), self.all_sprites, self.collision_sprites)

    def run(self, dt):
        self.display_surface.fill(BLACK)
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
        self.virtual_rect = self.virtual_surface.get_rect()

    def center_target_camera(self, target):
        self.offset.x = target.rect.centerx - (VIRTUAL_SCREEN_WIDTH // 2)
        self.offset.y = target.rect.centery - (VIRTUAL_SCREEN_HEIGHT // 2)

    def custom_draw(self, player):
        self.center_target_camera(player)
        self.virtual_surface.fill(BLACK)

        for layer in LAYERS.values():
            for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
                if sprite.z == layer:
                    offset_rect = sprite.rect.copy()
                    offset_rect.center -= self.offset
                    self.virtual_surface.blit(sprite.image, offset_rect)
        scaled_surf = pygame.transform.scale(self.virtual_surface, self.current_size)
        self.display_surface.blit(scaled_surf, self.virtual_rect)
