import pygame as pg
import sys
#import pytmx

from settings import *
from map import *
from player import *
from raycasting import *
from wall_renderer import *
from sprite import *
from animated_sprite import *
from sprite_handler import *
from weapon import *
from sound_handler import *

class Game:
    def __init__(self):
        pg.init()
        pg.mouse.set_visible(False)
        self.screen = pg.display.set_mode(RES)
        self.clock = pg.time.Clock()
        self.delta_time = 1
        self.new_game()
        self.is_minimap_visible = False
        #self.tmx_map = self.load_tiled_map("src/resources/maps/episode1-floor1.tmx")

    def new_game(self):
        self.map = Map(self)
        self.player = Player(self)
        self.wall_renderer = WallRenderer(self)
        self.raycasting = RayCasting(self)
        self.sprite_handler = SpriteHandler(self)
        self.weapon = Weapon(self)
        self.sound_handler = SoundHandler()
        
    def update(self):
        self.player.update()
        self.raycasting.update()
        self.weapon.update()
        self.sprite_handler.update()       
        pg.display.flip()
        self.delta_time = self.clock.tick(FPS)
        pg.display.set_caption(f'{self.clock.get_fps() :.1f}')
        
    def draw(self):
        self.wall_renderer.draw()
        if self.is_minimap_visible:
            self.map.draw()
            self.player.draw()
        self.weapon.draw()

    # def load_tiled_map(self, tmx_file):
    #     tmx_map = pytmx.TiledMap(tmx_file)
    #     return tmx_map      

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()
            self.player.single_fire_event(event)

    def run(self):
        while True:
            self.check_events()
            self.update()
            self.draw()
   
if __name__ == '__main__':
    game = Game()
    game.run()
 