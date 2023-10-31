import pygame as pg
from enum import Enum

class Sounds(Enum):
    PLAYER_KNIFE = 1
    PLAYER_PISTOL = 2
    PLAYER_RIFLE = 3
    PLAYER_MINUGUN = 4
    

class SoundHandler:
    def __init__(self):
        pg.mixer.init()
        self.sounds = {}
        self.load_sounds()

    def load_sounds(self):
        #self.sounds[Sounds.PLAYER_KNIFE] = pg.mixer.Sound('assets/sounds/knife-attack.ogg')
        self.sounds[Sounds.PLAYER_PISTOL] = pg.mixer.Sound('assets/sounds/pistol-fire.ogg')
        #self.sounds[Sounds.PLAYER_RIFLE] = pg.mixer.Sound('assets/sounds/rifle-fire.ogg')
        #self.sounds[Sounds.PLAYER_MINUGUN] = pg.mixer.Sound('assets/sounds/minigun-fire.ogg')

    def play_sound(self, sound_name):
        if sound_name in self.sounds:
            self.sounds[sound_name].play()
