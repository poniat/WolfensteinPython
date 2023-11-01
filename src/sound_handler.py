import pygame as pg
from sounds import *   

class SoundHandler:
    def __init__(self):
        pg.mixer.init()
        pg.mixer.set_num_channels(32)
        self.sounds = {}
        self.load_sounds()

    def load_sounds(self):
        self.sounds[Sounds.PLAYER_KNIFE] = pg.mixer.Sound('assets/sounds/knife.wav')
        self.sounds[Sounds.PLAYER_PISTOL] = pg.mixer.Sound('assets/sounds/pistol-fire.ogg')
        self.sounds[Sounds.PLAYER_RIFLE] = pg.mixer.Sound('assets/sounds/SmgFire.ogg')
        self.sounds[Sounds.PLAYER_MINIGUN] = pg.mixer.Sound('assets/sounds/ChaingunFire.ogg')
        self.sounds[Sounds.NPC_PAIN] = pg.mixer.Sound('assets/sounds/npc_pain.wav')
        self.sounds[Sounds.NPC_DEATH] = pg.mixer.Sound('assets/sounds/npc_death.wav')
        self.sounds[Sounds.NPC_PISTOL_FIRE] = pg.mixer.Sound('assets/sounds/EnemyPistolFire.ogg')

        self.sounds[Sounds.NPC_TALK_SCHUTZ_STAFFEL] = pg.mixer.Sound('assets/sounds/Schutzstaffel.ogg')
        self.sounds[Sounds.NPC_TALK_KOMM_HIER_SCHWEIN] = pg.mixer.Sound('assets/sounds/KommherrSchwien.ogg')
        self.sounds[Sounds.NPC_TALK_GUTEN_TAG] = pg.mixer.Sound('assets/sounds/Guten Tag.ogg')

        self.sounds[Sounds.AMMO] = pg.mixer.Sound('assets/sounds/ammo.wav')
        

    def play_sound(self, sound_name):
        if sound_name in self.sounds:
            self.sounds[sound_name].play()
