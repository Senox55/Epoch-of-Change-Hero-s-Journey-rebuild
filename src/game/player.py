import pygame
import os
from src.utils.settings import *
from src.utils.support import *
from src.utils.timer import Timer


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, group, collision_sprites):
        super().__init__(group)

        self.import_assets()
        self.status = 'down_idle'
        self.frame_index = 0

        # general setup
        self.image = self.movement_animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(center=pos)
        self.hitbox = self.rect.copy().inflate(-33, -27)
        print(self.hitbox)
        self.z = LAYERS['main']

        # movement attributes
        self.direction = pygame.math.Vector2()
        self.pos = pygame.math.Vector2(self.rect.center)
        self.speed = 200

        # animation attributes
        self.animation_speed = 10

        # collision
        self.collision_sprites = collision_sprites

        # timer
        self.timers = {
            'tool use': Timer(350, self.use_tool),
            'tool switch': Timer(600)
        }

        # tools
        self.tools = ['bronze_sword', 'simple_sword']
        self.tool_index = 0
        self.selected_tool = self.tools[self.tool_index]

    def use_tool(self):
        # print(self.selected_tool)
        pass

    def import_assets(self):
        self.movement_animations = {'up': [], 'down': [], 'left': [], 'right': [],
                                    'up_idle': [], 'down_idle': [], 'left_idle': [],
                                    'right_idle': []}
        self.attack_animations = {'up_bronze_sword': [], 'down_bronze_sword': [], 'left_bronze_sword': [],
                                  'right_bronze_sword': [], 'up_simple_sword': [], 'down_simple_sword': [],
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

    def input(self):
        keys = pygame.key.get_pressed()

        if not self.timers['tool use'].active:
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
                self.timers['tool use'].activate()
                self.direction = pygame.math.Vector2()
                self.frame_index = 0

            # change tool
            if keys[pygame.K_q] and not self.timers['tool switch'].active:
                self.timers['tool switch'].activate()
                self.tool_index += 1
                if self.tool_index >= len(self.tools):
                    self.tool_index = 0
                self.selected_tool = self.tools[self.tool_index]

    def get_status(self):

        # idle
        if self.direction.magnitude() == 0:
            self.status = self.status.split('_')[0] + '_idle'

        # tool use
        if self.timers['tool use'].active:
            self.status = self.status.split('_')[0] + '_' + self.selected_tool

    def update_timers(self):
        for timer in self.timers.values():
            timer.update()

    def collision(self, direction):
        for sprite in self.collision_sprites:
            if hasattr(sprite, 'hitbox'):
                if sprite.hitbox.colliderect(self.hitbox):
                    if direction == 'horizontal':
                        if self.direction.x > 0:  # moving right
                            self.hitbox.right = sprite.hitbox.left
                        if self.direction.x < 0:  # moving left
                            self.hitbox.left = sprite.hitbox.right
                        self.rect.centerx = self.hitbox.centerx
                        self.pos.x = self.hitbox.centerx
                    if direction == 'vertical':
                        if self.direction.y > 0:  # moving bottom
                            self.hitbox.bottom = sprite.hitbox.top
                        if self.direction.y < 0:  # moving top
                            self.hitbox.top = sprite.hitbox.bottom
                        self.rect.centery = self.hitbox.centery
                        self.pos.y = self.hitbox.centery

    def move(self, dt):

        # normalizing vector
        if self.direction.magnitude() > 0:
            self.direction = self.direction.normalize()

        # horizontal movement
        self.pos.x += self.direction.x * self.speed * dt
        self.hitbox.centerx = round(self.pos.x)
        self.rect.centerx = self.hitbox.centerx
        self.collision('horizontal')

        # vertical movement
        self.pos.y += self.direction.y * self.speed * dt
        self.hitbox.centery = round(self.pos.y)
        self.rect.centery = self.hitbox.centery
        self.collision('vertical')

    def update(self, dt):
        self.input()
        self.update_timers()
        self.get_status()

        self.move(dt)
        self.animate(dt)
