import random

import pygame
from src.utils.settings import *
from src.game.entity import Entity
from src.utils.timer import Timer
from src.utils.support import *


class Enemy(Entity):
    def __init__(self, monster_name, pos, groups, collision_sprites, damage_player, add_exp):
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
        self.action = 'idle'

        # hitbox attribute
        self.change_hitbox_x = monster_data[monster_name]['hitbox']['x']
        self.change_hitbox_y = monster_data[monster_name]['hitbox']['y']
        self.hitbox_width = monster_data[monster_name]['hitbox']['width']
        self.hitbox_height = monster_data[monster_name]['hitbox']['height']
        self.hitbox = pygame.Rect(self.rect.x + self.change_hitbox_x, self.rect.y + self.change_hitbox_y,
                                  self.hitbox_width,
                                  self.hitbox_height)

        # movement attributes
        self.pos = pygame.math.Vector2(self.rect.center)

        # collision
        self.collision_sprites = collision_sprites

        # timer
        self.timers = {
            'attacked cooldown': Timer(TIME_ATTACKING),
            'one mil': Timer(1),
            'death': Timer(1000)
        }

        # attack attributes
        self.can_attack = True
        self.vulnerable = True
        self.damage_player = damage_player

        # animation attributes
        self.animation_speed = 10

        # stats
        self.health = monster_data[monster_name]['health']
        self.damage = monster_data[monster_name]['damage']
        self.speed = monster_data[monster_name]['speed']
        self.attack_type = monster_data[monster_name]['attack_type']
        self.attack_radius = monster_data[monster_name]['attack_radius']
        self.notice_radius = monster_data[monster_name]['notice_radius']
        self.repulsion = monster_data[monster_name]['repulsion']
        self.exp = monster_data[monster_name]['exp']

        # death attributes
        self.death = False

        # exp attributes
        self.add_exp = add_exp

        # import sounds
        self.death_sound = pygame.mixer.Sound(r'..\Epoch-of-Change-Hero-s-Journey-rebuild\audio\death\slime_death.wav')

    def import_assets(self, name):
        self.movement_animations = {'up': [], 'down': [], 'left': [], 'right': [],
                                    'up_idle': [], 'down_idle': [], 'left_idle': [],
                                    'right_idle': [], 'death': []}

        for move_animation in self.movement_animations.keys():
            full_path = fr'..\Epoch-of-Change-Hero-s-Journey-rebuild\assets\enemy\{name}\movement/' + move_animation
            self.movement_animations[move_animation] = import_folder(full_path)

    def get_player_distance_direction(self, player):
        enemy_vec = pygame.math.Vector2(self.hitbox.center)
        player_vec = pygame.math.Vector2(player.hitbox.center)
        distance = (player_vec - enemy_vec).magnitude()
        if distance > 0:
            direction = (player_vec - enemy_vec).normalize()
        else:
            direction = pygame.math.Vector2()

        return (distance, direction)

    def actions(self, player):
        distance = self.get_player_distance_direction(player)[0]

        if distance <= self.attack_radius:
            self.action = 'attack'
        elif distance <= self.notice_radius:
            self.action = 'move'
        else:
            self.action = 'stay'

    def animate(self, dt):
        if self.timers['death'].active:
            self.frame_index += dt * (
                    (len(self.movement_animations[self.status]) * SECOND_TO_MILLISECOND) / self.timers[
                'death'].duration)
            if self.frame_index >= len(self.movement_animations[self.status]):
                self.kill()
                self.frame_index = 0
        else:
            self.frame_index += dt * self.animation_speed
            if self.frame_index >= len(self.movement_animations[self.status]):
                self.frame_index = 0
        self.image = self.movement_animations[self.status][int(self.frame_index)]

        if not self.vulnerable:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

    def get_status(self, player):

        if self.check_death():
            self.status = 'death'
            self.direction = pygame.math.Vector2()

        else:
            if self.action == 'attack':
                self.damage_player(self.damage, self.attack_type)

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

    def cooldowns(self):
        if self.timers['attacked cooldown'].active:
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
            if attack_type == 'weapon':
                self.health -= player.get_full_weapon_damage()

            elif attack_type == 'magic':
                self.health -= player.get_full_magic_damage()

            self.timers['attacked cooldown'].activate()
            self.vulnerable = False

    def check_death(self):
        if self.health <= 0:
            if not self.timers['death'].active and not self.death:
                self.death = True
                self.timers['death'].activate()
                self.frame_index = 0
                self.death_sound.play()
                self.add_exp(self.exp)

            return True

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
        self.cooldowns()
        self.check_death()

    def enemy_update(self, player):
        self.get_status(player)
        self.actions(player)
