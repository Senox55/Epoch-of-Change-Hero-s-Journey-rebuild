import random

import pygame
from src.utils.settings import *
from src.game.entity import Entity
from src.utils.timer import Timer
from src.utils.support import *


class Enemy(Entity):
    def __init__(self, monster_name, pos, groups, collision_sprites):
        # general setup
        super().__init__(groups)
        self.sprite_type = 'enemy'
        self.z = LAYERS['main']
        self.monster_name = monster_name

        # graphics setup
        self.status = 'down_idle'
        self.import_assets(monster_name)
        self.image = self.movement_animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(center=pos)
        self.hitbox = self.rect.inflate(-10, -10)
        self.action = 'idle'

        # movement attributes
        self.pos = pygame.math.Vector2(self.rect.center)

        # collision
        self.collision_sprites = collision_sprites

        # timer
        self.timers = {
            'attack cooldown': Timer(TIME_ATTACKING),
            'one mil': Timer(1)
        }

        # attack attributes
        self.can_attack = True
        self.vulnerable = True

        # animation attributes
        self.animation_speed = 10

        # stats
        self.health = monster_data[monster_name]['health']
        self.speed = monster_data[monster_name]['speed']
        self.attack_radius = monster_data[monster_name]['attack_radius']
        self.notice_radius = monster_data[monster_name]['notice_radius']
        self.repulsion = monster_data[monster_name]['repulsion']

    def import_assets(self, name):
        self.movement_animations = {'up': [], 'down': [], 'left': [], 'right': [],
                                    'up_idle': [], 'down_idle': [], 'left_idle': [],
                                    'right_idle': []}

        for move_animation in self.movement_animations.keys():
            full_path = fr'..\Epoch-of-Change-Hero-s-Journey-rebuild\assets\enemy\{self.monster_name}\movement/' + move_animation
            self.movement_animations[move_animation] = import_folder(full_path)

    def get_player_distance_direction(self, player):
        enemy_vec = pygame.math.Vector2(self.rect.center)
        player_vec = pygame.math.Vector2(player.rect.center)
        distance = (player_vec - enemy_vec).magnitude()
        if distance > 0:
            direction = (player_vec - enemy_vec).normalize()
        else:
            direction = pygame.math.Vector2()

        return (distance, direction)

    def get_status(self, player):
        distance = self.get_player_distance_direction(player)[0]

        if distance <= self.attack_radius:
            self.action = 'attack'
        elif distance <= self.notice_radius:
            self.action = 'move'
        else:
            self.action = 'stay'

    def animate(self, dt):
        self.frame_index += dt * self.animation_speed
        if self.frame_index >= len(self.movement_animations[self.status]):
            self.frame_index = 0
        self.image = self.movement_animations[self.status][int(self.frame_index)]

        if not self.vulnerable:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

    def actions(self, player):
        if self.action == 'attack':
            if not self.timers['attack cooldown'].active:
                print('attack')
                self.timers['attack cooldown'].activate()
        elif self.action == 'move':
            self.direction = self.get_player_distance_direction(player)[1]
            if abs(self.direction.y) > abs(self.direction.x):
                if self.direction.y > 0:
                    self.status = 'down'
                else:
                    self.status = 'up'

            if abs(self.direction.x) > abs(self.direction.y):
                if self.direction.x > 0:
                    self.status = 'right'
                else:
                    self.status = 'left'
        elif self.action == 'stay':
            self.status = 'down_idle'
            self.direction = pygame.math.Vector2()

    def cooldown(self):
        if self.timers['attack cooldown'].active:
            self.timers['one mil'].activate()
        if not self.can_attack:
            if not self.timers['one mil'].active:
                self.can_attack = True

        if not self.vulnerable:
            if not self.timers['one mil'].active:
                self.vulnerable = True

    def get_damage(self, player, attack_type):
        if self.vulnerable:
            self.direction = self.get_player_distance_direction(player)[1]
            if attack_type == 'attack':
                self.health -= player.damage
                self.timers['attack cooldown'].activate()
            self.vulnerable = False

    def check_death(self):
        if self.health <= 0:
            self.kill()

    def hit_reaction(self):
        if not self.vulnerable:
            self.direction *= -self.repulsion

    def update_timers(self):
        for timer in self.timers.values():
            timer.update()

    def update(self, dt):
        self.hit_reaction()
        self.move(dt)
        self.animate(dt)
        self.update_timers()
        self.cooldown()
        self.check_death()

    def enemy_update(self, player):
        self.get_status(player)
        self.actions(player)
