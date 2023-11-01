import pygame as pg
from settings import *
from pytmx import *
from main import *

class ObjectRenderer:
    def __init__(self, game: Game):
        self.game = game
        self.screen = game.screen
        self.wall_textures = self.load_wall_textures()
        self.sky_image = self.get_texture('assets/textures/sky1.png', (WIDTH, HALF_HEIGHT))
        self.sky_offset = 0
        self.blood_screen = self.get_texture('assets/textures/blood_screen.png', RESOLUTION)
        self.digit_width = 8 * GAME_SCALE
        self.digit_height = 16 * GAME_SCALE
        self.digit_images = [self.get_texture(f'assets/textures/hud-digits/{i}.png', (self.digit_width, self.digit_height))
                             for i in range(10)]
        self.digit = dict(zip(map(str, range(10)), self.digit_images))
        self.hud_background_image = self.get_texture('assets/textures/hud_background.png', (320 * GAME_SCALE, 40 * GAME_SCALE))
        self.game_over_image = self.get_texture('assets/textures/game_over.png', RESOLUTION)

    def draw(self):
        self.draw_background()
        self.render_game_objects()
        self.draw_hud()
        

    def draw_hud(self):
        self.screen.blit(self.hud_background_image, (HALF_WIDTH - self.hud_background_image.get_width() // 2, HEIGHT - self.hud_background_image.get_height()))
        self.draw_player_health()

    def draw_player_health(self):
        health = str(self.game.player.health)[::-1]
        for i, char in enumerate(health):
            self.screen.blit(self.digit[char], ((183 * GAME_SCALE - self.digit_width * i), 176 * GAME_SCALE))
    
    def game_over(self):
        self.screen.blit(self.game_over_image, (0, 0))

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
    
    def player_damage(self):
        self.screen.blit(self.blood_screen, (0, 0))
