import pygame as pg
from settings import *

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
        return {
            1: self.get_texture('assets/textures/wood_wall.png'),
            2: self.get_texture('assets/textures/wood_wall_eagle.png'),
            3: self.get_texture('assets/textures/wood_wall_hitler.png'),
            4: self.get_texture('assets/textures/blue_wall_brick.png'),
            5: self.get_texture('assets/textures/wall_1_64.png'),
            6: self.get_texture('assets/textures/wall_2_64.png'),
            7: self.get_texture('assets/textures/wall_3_64.png'),
            8: self.get_texture('assets/textures/wall_4_64.png'),
            9: self.get_texture('assets/textures/blue_wall_brick_verboten.png'),
            10: self.get_texture('assets/textures/blue_wall_brick_cage.png'),
            11: self.get_texture('assets/textures/blue_wall_brick_cage_bones.png'),
            12: self.get_texture('assets/textures/door_front.png'),
            13: self.get_texture('assets/textures/door_left.png'),
            14: self.get_texture('assets/textures/door_right.png'),            
        }