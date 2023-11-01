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
        self.hud_knife_image = self.get_texture('assets/textures/hud_knife.png', (48 * GAME_SCALE, 24 * GAME_SCALE))
        self.hud_pistol_image = self.get_texture('assets/textures/hud_pistol.png', (48 * GAME_SCALE, 24 * GAME_SCALE))
        self.hud_rifle_image = self.get_texture('assets/textures/hud_rifle.png', (48 * GAME_SCALE, 24 * GAME_SCALE))
        self.hud_minigun_image = self.get_texture('assets/textures/hud_minigun.png', (48 * GAME_SCALE, 24 * GAME_SCALE))

        self.hud_gold_key_image = self.get_texture('assets/textures/hud_gold_key.png', (8 * GAME_SCALE, 16 * GAME_SCALE))
        self.hud_silver_key_image = self.get_texture('assets/textures/hud_silver_key.png', (8 * GAME_SCALE, 16 * GAME_SCALE))

        self.hud_player_face_damage_0 = self.get_texture('assets/textures/hud_player_health_0.png', (24 * GAME_SCALE, 32 * GAME_SCALE))
        self.hud_player_face_damage_1 = self.get_texture('assets/textures/hud_player_health_1.png', (24 * GAME_SCALE, 32 * GAME_SCALE))
        self.hud_player_face_damage_2 = self.get_texture('assets/textures/hud_player_health_2.png', (24 * GAME_SCALE, 32 * GAME_SCALE))
        self.hud_player_face_damage_3 = self.get_texture('assets/textures/hud_player_health_3.png', (24 * GAME_SCALE, 32 * GAME_SCALE))
        self.hud_player_face_damage_4 = self.get_texture('assets/textures/hud_player_health_4.png', (24 * GAME_SCALE, 32 * GAME_SCALE))
        self.hud_player_face_damage_5 = self.get_texture('assets/textures/hud_player_health_5.png', (24 * GAME_SCALE, 32 * GAME_SCALE))
        self.hud_player_face_damage_6 = self.get_texture('assets/textures/hud_player_health_6.png', (24 * GAME_SCALE, 32 * GAME_SCALE))
        self.hud_player_face_damage_7 = self.get_texture('assets/textures/hud_player_health_7.png', (24 * GAME_SCALE, 32 * GAME_SCALE))

    def draw(self):
        self.draw_background()
        self.render_game_objects()
        self.draw_hud()
        

    def draw_hud(self):
        self.screen.blit(self.hud_background_image, (HALF_WIDTH - self.hud_background_image.get_width() // 2, HEIGHT - self.hud_background_image.get_height()))
        self.draw_player_floor()
        self.draw_player_score()
        self.draw_player_lives()
        self.draw_player_health()
        self.draw_player_ammo()
        self.draw_player_keys()
        self.draw_player_weapon()

    def draw_player_floor(self):
        floor = str(self.game.player.floor)[::-1]
        for i, char in enumerate(floor):
            self.screen.blit(self.digit[char], ((22 * GAME_SCALE - self.digit_width * i), 176 * GAME_SCALE))
        
    def draw_player_score(self):
        score = str(self.game.player.score)[::-1]
        for i, char in enumerate(score):
            self.screen.blit(self.digit[char], ((88 * GAME_SCALE - self.digit_width * i), 176 * GAME_SCALE))
        
    def draw_player_lives(self):
        if self.game.player.lives < 0:
            lives = '0'
        else:
            lives = str(self.game.player.lives)[::-1]
        for i, char in enumerate(lives):
            self.screen.blit(self.digit[char], ((112 * GAME_SCALE - self.digit_width * i), 176 * GAME_SCALE))

    def draw_player_health(self):
        if self.game.player.health < 0:
            health = '0'
            self.screen.blit(self.hud_player_face_damage_0, (135 * GAME_SCALE, 164 * GAME_SCALE))
        else:
            health = str(self.game.player.health)[::-1]
        for i, char in enumerate(health):
            self.screen.blit(self.digit[char], ((183 * GAME_SCALE - self.digit_width * i), 176 * GAME_SCALE))
            if self.game.player.health == 100:
                self.screen.blit(self.hud_player_face_damage_7, (135 * GAME_SCALE, 164 * GAME_SCALE))
            elif self.game.player.health > 80:
                self.screen.blit(self.hud_player_face_damage_6, (135 * GAME_SCALE, 164 * GAME_SCALE))
            elif self.game.player.health > 60:
                self.screen.blit(self.hud_player_face_damage_5, (135 * GAME_SCALE, 164 * GAME_SCALE))
            elif self.game.player.health > 45:
                self.screen.blit(self.hud_player_face_damage_4, (135 * GAME_SCALE, 164 * GAME_SCALE))
            elif self.game.player.health > 30:
                self.screen.blit(self.hud_player_face_damage_3, (135 * GAME_SCALE, 164 * GAME_SCALE))
            elif self.game.player.health > 15:
                self.screen.blit(self.hud_player_face_damage_2, (135 * GAME_SCALE, 164 * GAME_SCALE))
            elif self.game.player.health > 0:
                self.screen.blit(self.hud_player_face_damage_1, (135 * GAME_SCALE, 164 * GAME_SCALE))

    def draw_player_ammo(self):
        if self.game.player.ammo < 0:
            ammo = '0'
        else:
            ammo = str(self.game.player.ammo)[::-1]
        for i, char in enumerate(ammo):
            self.screen.blit(self.digit[char], ((221 * GAME_SCALE - self.digit_width * i), 176 * GAME_SCALE))

    def draw_player_keys(self):
        if self.game.player.found_gold_key:
            self.screen.blit(self.hud_gold_key_image, (240 * GAME_SCALE, 164 * GAME_SCALE))
        if self.game.player.found_silver_key:
            self.screen.blit(self.hud_silver_key_image, (240 * GAME_SCALE, 181 * GAME_SCALE))

    def draw_player_weapon(self):
        if self.game.player.active_weapon == Weapons.KNIFE:
            self.screen.blit(self.hud_knife_image, (255 * GAME_SCALE, 168 * GAME_SCALE))

        elif self.game.player.active_weapon == Weapons.PISTOL:
            self.screen.blit(self.hud_pistol_image, (255 * GAME_SCALE, 168 * GAME_SCALE))

        elif self.game.player.active_weapon == Weapons.RIFLE:
            self.screen.blit(self.hud_rifle_image, (255 * GAME_SCALE, 168 * GAME_SCALE))

        elif self.game.player.active_weapon == Weapons.MINIGUN:
            self.screen.blit(self.hud_minigun_image, (255 * GAME_SCALE, 168 * GAME_SCALE))
    
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
