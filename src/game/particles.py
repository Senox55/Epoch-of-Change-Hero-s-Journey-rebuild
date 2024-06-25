import pygame
from src.utils.support import import_folder
from src.utils.settings import *
from src.utils.timer import Timer


class AnimationPlayer:
    def __init__(self):
        self.frames = {
            # magic
            'flame': import_folder(r'..\Epoch-of-Change-Hero-s-Journey-rebuild\assets\particles/fire'),
            'heal': import_folder(r'..\Epoch-of-Change-Hero-s-Journey-rebuild\assets\particles/heal')
        }

    def reflect_images(self, frames):
        pass

    def create_particles(self, animation_type, pos, groups):
        animation_frames = self.frames[animation_type]
        ParticleEffect(pos, animation_frames, groups)


class ParticleEffect(pygame.sprite.Sprite):
    def __init__(self, pos, animation_frames, groups):
        super().__init__(groups)
        self.frame_index = 0
        self.sprite_type = 'magic'
        self.animation_speed = 15
        self.frames = animation_frames
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center=pos)
        self.z = LAYERS['main']

        self.timers = {'magic use': Timer(TIME_HEALING)}

    def animate(self, dt):
        self.frame_index += dt * (
                (len(self.frames) * SECOND_TO_MILLISECOND) / self.timers[
            'magic use'].duration)
        if self.frame_index >= len(self.frames):
            self.kill()
        else:
            self.image = self.frames[int(self.frame_index)]

    def update(self, dt):
        self.animate(dt)
