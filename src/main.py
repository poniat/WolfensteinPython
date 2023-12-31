import pygame as pg
import sys
import pytmx

from settings import *
from map import *
from player import *
from raycasting import *
from object_renderer import *
from sprite import *
from animated_sprite import *
from sprite_handler import *
from weapon import *
from sound_handler import *
from npc import *

class Game:
    def __init__(self):
        pg.init()
        pg.mouse.set_visible(False)
        self.screen = pg.display.set_mode(RESOLUTION)
        #self.screen = pg.display.set_mode(RESOLUTION, pg.FULLSCREEN)

        self.clock = pg.time.Clock()
        self.delta_time = 1
        self.tmx_map = self.load_tiled_map("assets/maps/episode1-floor1.tmx")
        self.is_minimap_visible = False
        self.new_game()

    def restart_floor(self):
        self.sprite_handler = SpriteHandler(self)
        self.player.restart()
        

    def new_game(self):        
        self.map = Map(self)
        self.player = Player(self)
        self.object_renderer = ObjectRenderer(self)
        self.raycasting = RayCasting(self)
        self.sprite_handler = SpriteHandler(self)
        self.pistol = Weapon(self, 'pistol')
        self.knife = Knife(self, 'knife')
        self.rifle = Rifle(self, 'rifle')
        self.minigun = Minigun(self, 'minigun')
        self.weapon = self.pistol
        self.sound_handler = SoundHandler()
        #self.npc = Npc(self, 'npc')
        
    def update(self):
        self.player.update()
        self.raycasting.update()
        self.weapon.update()
        self.sprite_handler.update()       
        pg.display.flip()
        self.delta_time = self.clock.tick(FPS)
        pg.display.set_caption(f'{self.clock.get_fps() :.1f}')
        
    def draw(self):
        if IS_2D_MODEL_ENABLED:
            self.screen.fill('black')
            self.map.draw()
            self.player.draw()
            self.weapon.draw()
        else:
            self.weapon.draw()
            self.object_renderer.draw()
            if self.is_minimap_visible:
                self.map.draw()
                self.player.draw()
        
        

    def load_tiled_map(self, tmx_file):
        tmx_map = pytmx.TiledMap(tmx_file)
        return tmx_map      

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                self.quit()
            #self.player.single_fire_event(event)
            #self.player.attack_event(event)

    def run(self):
        while True:
            self.check_events()
            self.update()
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()
        
if __name__ == '__main__':
    game = Game()
    game.run()
 