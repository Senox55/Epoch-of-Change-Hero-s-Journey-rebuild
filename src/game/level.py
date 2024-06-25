import pygame
from src.utils.settings import *
from src.game.player import Player
from src.game.enemy import Enemy
from src.game.overlay import Overlay
from src.game.sprites import Generic, Tree, Bush, Coffin
from src.game.attack import Attack
from pytmx.util_pygame import load_pygame


class Level:
    def __init__(self):
        # get the display surface
        self.display_surface = pygame.display.get_surface()

        # sprite groups
        self.all_sprites = CameraGroup()
        self.collision_sprites = pygame.sprite.Group()

        # attack sprites
        self.current_attack = None
        self.attack_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()

        self.setup()
        self.overlay = Overlay(self.player)

    def setup(self):
        tmx_data = load_pygame(r'..\Epoch-of-Change-Hero-s-Journey-rebuild\data\map.tmx')

        # ground
        for x, y, surf in tmx_data.get_layer_by_name('ground').tiles():
            pos = (x * TILESIZE, y * TILESIZE)
            Generic(pos, surf, 'ground', [self.all_sprites], LAYERS['ground'])

        # blocks
        for x, y, surf in tmx_data.get_layer_by_name('blocks').tiles():
            pos = (x * TILESIZE, y * TILESIZE)
            Generic(pos, surf, 'blocks', [self.all_sprites, self.collision_sprites])

        # coffin
        for obj in tmx_data.get_layer_by_name('props'):
            pos = (obj.x, obj.y)
            Coffin(pos, obj.image, 'coffin', groups=[self.all_sprites, self.collision_sprites])

        # bushes
        for obj in tmx_data.get_layer_by_name('bushes'):
            pos = (obj.x, obj.y)
            Bush(pos, obj.image, 'bushes',
                 groups=[self.all_sprites, self.collision_sprites, self.attackable_sprites])

        # entity
        for obj in tmx_data.get_layer_by_name('enemy'):
            pos = (obj.x, obj.y)
            Enemy(obj.name, pos, [self.all_sprites, self.attackable_sprites], self.collision_sprites,
                  self.damage_player)

        # player
        for obj in tmx_data.get_layer_by_name('player'):
            pos = (obj.x, obj.y)
            self.player = Player(pos, self.all_sprites, self.collision_sprites, self.create_attack, self.destroy_attack)

    def create_attack(self):
        self.current_attack = Attack(self.player, [self.attack_sprites])

    def destroy_attack(self):
        if self.current_attack:
            self.current_attack.kill()
        self.current_attack = None

    def player_attack_logic(self):
        if self.attack_sprites:
            for attack_sprite in self.attack_sprites:
                for target_sprite in self.attackable_sprites:
                    if attack_sprite.rect.colliderect(target_sprite.hitbox):
                        if target_sprite.sprite_type == 'bushes':
                            target_sprite.kill()
                        elif target_sprite.sprite_type == 'enemy':
                            target_sprite.get_damage(self.player, attack_sprite.sprite_type)

    def damage_player(self, amount, attack_type):
        if self.player.vulnerable:
            self.player.health -= amount
            self.player.vulnerable = False

    def run(self, dt):
        self.display_surface.fill(BLACK)
        self.all_sprites.custom_draw(self.player)
        self.all_sprites.update(dt)
        self.all_sprites.enemy_update(self.player)
        self.player_attack_logic()

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

    def draw_hitbox(self, sprite):
        hitbox_rect = sprite.hitbox.copy()
        hitbox_rect.center -= self.offset
        pygame.draw.rect(self.virtual_surface, RED, hitbox_rect, 1)

    def custom_draw(self, player):
        self.center_target_camera(player)
        self.virtual_surface.fill(BLACK)

        for layer in LAYERS.values():
            for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
                if sprite.z == layer:
                    offset_rect = sprite.rect.copy()
                    offset_rect.center -= self.offset
                    self.virtual_surface.blit(sprite.image, offset_rect)
                    # if hasattr(sprite, 'hitbox'):
                    #     self.draw_hitbox(sprite)

        scaled_surf = pygame.transform.scale(self.virtual_surface, self.current_size)
        self.display_surface.blit(scaled_surf, self.virtual_rect)

    def enemy_update(self, player):
        enemy_sprites = [sprite for sprite in self.sprites() if
                         hasattr(sprite, 'sprite_type') and sprite.sprite_type == 'enemy']
        for enemy in enemy_sprites:
            enemy.enemy_update(player)
