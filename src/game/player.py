import sys
import random
import pygame
import os
from src.utils.settings import *
from src.utils.support import *
from src.utils.timer import Timer
from src.game.entity import Entity


class Player(Entity):
    def __init__(self, pos, groups, collision_sprites, create_attack, destroy_attack, create_magic):

        # general setup
        super().__init__(groups)

        # graphics setup
        self.import_assets()
        self.status = 'down_idle'
        self.image = self.movement_animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(center=pos)
        self.hitbox = self.rect.inflate(-30, -30)
        self.z = LAYERS['main']

        # movement attributes
        self.pos = pygame.math.Vector2(self.rect.center)

        # animation attributes
        self.animation_speed = 8

        # collision
        self.collision_sprites = collision_sprites

        # attack attributes
        self.create_attack = create_attack
        self.destroy_attack = destroy_attack
        self.create_magic = create_magic
        self.vulnerable = True

        # timer
        self.timers = {
            'tool use': Timer(TIME_ATTACKING),
            'tool switch': Timer(600),
            'attacked cooldown': Timer(600, self.activate_vulnerable),
            'one millisecond': Timer(1, self.destroy_attack),
            'magic use': Timer(TIME_HEALING),
            'magic switch': Timer(600)
        }

        # weapon
        self.weapons = weapons_data
        self.weapon_index = 0
        self.weapon = list(weapons_data.keys())[self.weapon_index]

        # magic
        self.magics = magics_data
        self.magic_index = 0
        self.magic = list(magics_data.keys())[self.magic_index]

        # stats
        self.stats = {'health': 100, 'damage': 2, 'speed': 100, 'energy': 50, 'exp': 0}
        self.health = self.stats['health']
        self.energy = self.stats['energy']
        self.damage = self.stats['damage']
        self.speed = self.stats['speed']
        self.exp = self.stats['exp']
        self.death = False

        # import sounds
        self.weapon_attack_sound = pygame.mixer.Sound(
            r'..\Epoch-of-Change-Hero-s-Journey-rebuild\audio\attack\sword.wav')
        self.weapon_attack_sound.set_volume(0.4)

        self.player_death_sound = pygame.mixer.Sound(
            r'..\Epoch-of-Change-Hero-s-Journey-rebuild\audio\death\player_death.wav')

    def import_assets(self):
        self.movement_animations = {'up': [], 'down': [], 'left': [], 'right': [],
                                    'up_idle': [], 'down_idle': [], 'left_idle': [],
                                    'right_idle': []}
        self.attack_animations = {'up_katana': [], 'down_katana': [], 'left_katana': [],
                                  'right_katana': [], 'up_simple_sword': [], 'down_simple_sword': [],
                                  'left_simple_sword': [],
                                  'right_simple_sword': []}

        for attack_animation in self.attack_animations.keys():
            full_path = r'..\Epoch-of-Change-Hero-s-Journey-rebuild\assets\player\attack/' + attack_animation
            self.attack_animations[attack_animation] = import_folder(full_path)

        for move_animation in self.movement_animations.keys():
            full_path = r'..\Epoch-of-Change-Hero-s-Journey-rebuild\assets\player\movement/' + move_animation
            self.movement_animations[move_animation] = import_folder(full_path)

    def animate(self, dt):
        if self.timers['tool use'].active:
            self.frame_index += dt * (
                    (len(self.attack_animations[self.status]) * SECOND_TO_MILLISECOND) / self.timers[
                'tool use'].duration)
            if self.frame_index >= len(self.attack_animations[self.status]):
                self.frame_index = 0
            self.image = self.attack_animations[self.status][int(self.frame_index)]
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

    def get_full_weapon_damage(self):
        base_damage = self.stats['damage']
        weapon_damage = self.weapons[self.weapon]['damage']
        return base_damage + weapon_damage

    def get_full_magic_damage(self):
        base_damage = self.stats['damage']
        magic_damage = self.magics[self.magic]['strength']
        return base_damage + magic_damage

    def input(self):
        keys = pygame.key.get_pressed()

        if not self.timers['tool use'].active and not self.timers['magic use'].active:
            # directions
            if keys[pygame.K_w]:
                self.direction.y = -1
                self.status = 'up'
            elif keys[pygame.K_s]:
                self.direction.y = 1
                self.status = 'down'
            else:
                self.direction.y = 0

            if keys[pygame.K_d]:
                self.direction.x = 1
                self.status = 'right'
            elif keys[pygame.K_a]:
                self.direction.x = -1
                self.status = 'left'
            else:
                self.direction.x = 0

            # tool use
            if keys[pygame.K_SPACE]:
                self.weapon_attack_sound.play()
                self.create_attack()
                self.timers['tool use'].activate()
                self.timers['one millisecond'].activate()
                self.direction = pygame.math.Vector2()
                self.frame_index = 0

            # switch tool
            if keys[pygame.K_q] and not self.timers['tool switch'].active:
                self.timers['tool switch'].activate()
                self.weapon_index += 1
                if self.weapon_index >= len(self.weapons):
                    self.weapon_index = 0
                self.weapon = list(weapons_data.keys())[self.weapon_index]

            # use magic
            if keys[pygame.K_f]:
                self.create_magic(*self.magics[self.magic].values())
                self.timers['magic use'].activate()
                self.timers['one millisecond'].activate()
                self.direction = pygame.math.Vector2()
                self.frame_index = 0

            # switch magic
            if keys[pygame.K_z] and not self.timers['magic switch'].active:
                self.timers['magic switch'].activate()
                self.magic_index += 1
                if self.magic_index >= len(self.magics):
                    self.magic_index = 0
                self.magic = list(magics_data.keys())[self.magic_index]

    def get_status(self):

        # idle
        if self.direction.magnitude() == 0:
            self.status = self.status.split('_')[0] + '_idle'

        # tool use
        if self.timers['tool use'].active:
            self.status = self.status.split('_')[0] + '_' + self.weapon

    def activate_vulnerable(self):
        self.vulnerable = True

    def cooldowns(self):
        if not (self.timers['attacked cooldown'].active):
            self.timers['attacked cooldown'].activate()

    def check_death(self):
        if self.health <= 0 and not self.death:
            self.player_death_sound.play()
            self.death = True
            return True

    def update_timers(self):
        for timer in self.timers.values():
            timer.update()

    def update(self, dt):
        self.input()
        self.update_timers()
        self.get_status()
        self.cooldowns()
        self.check_death()

        self.move(dt)
        self.animate(dt)
