import pygame as pg
import os

from sprite import *
from settings import *
from collections import deque


class AnimatedSprite(Sprite):
    def __init__(self, game, path='assets/sprites/animated/green_light/0.png',
                 position=(39.5, 57.5), scale=0.8, shift=0.15, animation_time=120):
        super().__init__(game, path, position, scale, shift)
        self.animation_time = animation_time
        self.path = path.rsplit('/', 1)[0]
        self.images = self.get_images(self.path)
        self.animation_time_prev = pg.time.get_ticks()
        self.animation_trigger = False

    def update(self):
        super().update()
        self.check_animation_time()
        self.animate(self.images)

    def animate(self, images):
        if self.animation_trigger:
            images.rotate(-1)
            self.image = images[0]

    def check_animation_time(self):
        self.animation_trigger = False
        time_now = pg.time.get_ticks()
        if time_now - self.animation_time_prev > self.animation_time:
            self.animation_time_prev = time_now
            self.animation_trigger = True

    def get_images(self, path):
        images = deque()
        for file_name in os.listdir(path):
            if(os.path.isfile(os.path.join(path, file_name))):
                img = pg.image.load(path + '/' + file_name).convert_alpha()
                images.append(img)
        return images