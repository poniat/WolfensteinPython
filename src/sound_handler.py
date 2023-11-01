import pygame as pg
from sounds import *   

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
        self.sounds[Sounds.NPC_PAIN] = pg.mixer.Sound('assets/sounds/npc_pain.wav')
        self.sounds[Sounds.NPC_DEATH] = pg.mixer.Sound('assets/sounds/npc_death.wav')
        self.sounds[Sounds.NPC_PISTOL_FIRE] = pg.mixer.Sound('assets/sounds/EnemyPistolFire.ogg')

        self.sounds[Sounds.NPC_TALK_SCHUTZ_STAFFEL] = pg.mixer.Sound('assets/sounds/Schutzstaffel.ogg')
        self.sounds[Sounds.NPC_TALK_KOMM_HIER_SCHWEIN] = pg.mixer.Sound('assets/sounds/KommherrSchwien.ogg')
        self.sounds[Sounds.NPC_TALK_GUTEN_TAG] = pg.mixer.Sound('assets/sounds/Guten Tag.ogg')
        

    def play_sound(self, sound_name):
        if sound_name in self.sounds:
            self.sounds[sound_name].play()
