import pygame as pg
from settings import *
from pytmx import *

class WallRenderer:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.wall_textures = self.load_wall_textures()
        self.sky_image = self.get_texture('assets/textures/sky1.png', (WIDTH, HALF_HEIGHT))
        self.sky_offset = 0

    def draw(self):
        self.draw_background()
        self.render_game_objects()

    def draw_background(self):
        #sky
        self.sky_offset = (self.sky_offset + 4.5 * self.game.player.rel) % WIDTH
        self.screen.blit(self.sky_image, (-self.sky_offset, 0))
        self.screen.blit(self.sky_image, (-self.sky_offset + WIDTH, 0))
        #floor
        pg.draw.rect(self.screen, FLOOR_COLOR, (0, HALF_HEIGHT, WIDTH, HEIGHT))

    def render_game_objects(self):
        list_objects = sorted(self.game.raycasting.objects_to_render, key=lambda t: t[0], reverse=True)
        for depth, image, pos in list_objects:
            self.screen.blit(image, pos)

    @staticmethod
    def get_texture(path, res=(TEXTURE_SIZE, TEXTURE_SIZE)):
        texture = pg.image.load(path).convert_alpha()
        return pg.transform.scale(texture, res)
    
    def load_wall_textures(self):
        result = {}
        tmx_map = pytmx.TiledMap("assets/maps/episode1-floor1.tmx") 
        tile_properties = tmx_map.tile_properties

        for tile_id in tile_properties:
            if tile_id not in result:
                tile_prop = tile_properties[tile_id]
                asset_path = tile_prop['source']
                final_path = asset_path.replace('..', 'assets')
                result[tile_id] = self.get_texture(final_path)
        return result