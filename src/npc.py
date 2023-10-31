from animated_sprite import *
from random import randint, random, choice
from main import *

class Npc(AnimatedSprite):
    def __init__(self, game: Game, path='../assets/sprites/npc/guard/walk/0.png',
                 pos=(35.5, 61.5),
                 scale=1.0,
                 shift=0.0,
                 animation_time=180):
        super().__init__(game, path, pos, scale, shift, animation_time)