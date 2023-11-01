from settings import *
import pygame as pg
import math
from sound_handler import *
from weapons import *
from main import *

class Player:
    def __init__(self, game: Game):
        self.game = game
        self.x, self.y = self.get_starting_position(self.game.tmx_map)
        self.angle = PLAYER_ANGLE
        self.shot = False
        self.size = PLAYER_SIZE
        self.health = PLAYER_MAX_HEALTH
        self.lives = 3
        self.weapon_knife = True
        self.weapon_pistol = True
        self.weapon_rifle = False
        self.weapon_minigun = False
        self.active_weapon = Weapons.PISTOL
        self.episode = 1
        self.floor = 1
        self.score = 0
        self.ammo = 8
        self.found_gold_key = False
        self.found_silver_key = False
        self.rel = 0
        self.shoot_continuous = False
        self.last_shot_time = 0

    def update(self):
        self.movement()
        self.mouse_control()
        self.change_weapon()
        self.attack()

    def attack(self):
        mouse_buttons = pg.mouse.get_pressed()
        if mouse_buttons[0]:
            if not self.shot and not self.game.weapon.is_reloading:
                if self.active_weapon == Weapons.KNIFE:
                    self.play_active_weapon_sound()
                    self.shot = True
                    self.game.weapon.is_reloading = True
                elif self.ammo > 0:
                    self.ammo -= 1
                    self.play_active_weapon_sound()
                    self.shot = True
                    self.game.weapon.is_reloading = True
            
    def play_active_weapon_sound(self):
        if self.active_weapon == Weapons.KNIFE:
            self.game.sound_handler.play_sound(Sounds.PLAYER_KNIFE)
        elif self.active_weapon == Weapons.PISTOL:
            self.game.sound_handler.play_sound(Sounds.PLAYER_PISTOL)
        elif self.active_weapon == Weapons.RIFLE:
            self.game.sound_handler.play_sound(Sounds.PLAYER_RIFLE)
        elif self.active_weapon == Weapons.MINIGUN:
            self.game.sound_handler.play_sound(Sounds.PLAYER_MINIGUN)

    def restart(self):
        self.health = PLAYER_MAX_HEALTH
        self.ammo = 8
        self.active_weapon = Weapons.PISTOL
        self.game.weapon = self.game.pistol
        self.found_gold_key = False
        self.found_silver_key = False
        self.x, self.y = self.get_starting_position(self.game.tmx_map)
        self.angle = PLAYER_ANGLE
        

    def check_game_over(self):
        if self.health < 1:
            self.lives -= 1
            if self.lives > 0:
                self.game.object_renderer.game_over()
                pg.display.flip()
                pg.time.delay(2000)
                self.game.restart_floor()
            else:
                self.game.quit()

    def movement(self):
        sin_a = math.sin(self.angle)
        cos_a = math.cos(self.angle)
        dx, dy = 0, 0
        speed = PLAYER_SPEED * self.game.delta_time
        speed_sin = speed * sin_a
        speed_cos = speed * cos_a

        keys = pg.key.get_pressed()
        if keys[pg.K_w]:
            dx += speed_cos
            dy += speed_sin
        if keys[pg.K_s]:
            dx += -speed_cos
            dy += -speed_sin
        if keys[pg.K_a]:
            dx += speed_sin
            dy += -speed_cos
        if keys[pg.K_d]:
            dx += -speed_sin
            dy += speed_cos

        #run
        if keys[pg.K_LSHIFT]:
            dx *= 2
            dy *= 2

        #crawl
        if keys[pg.K_LCTRL]:
            dx /= 2
            dy /= 2

        if keys[pg.K_m]:
            self.game.is_minimap_visible = not self.game.is_minimap_visible

        self.check_wall_collision(dx, dy)
        self.check_sprite_collision(dx, dy)

        if keys[pg.K_LEFT]:
            self.angle -= PLAYER_ROTATION_SPEED * self.game.delta_time
        if keys[pg.K_RIGHT]:
            self.angle += PLAYER_ROTATION_SPEED * self.game.delta_time
        self.angle %= math.tau

    def check_wall(self, x, y):
        return (x, y) not in self.game.map.world_map

    def check_wall_collision(self, dx, dy):
        scale = PLAYER_SIZE / self.game.delta_time
        if self.check_wall(int(self.x + dx * scale), int(self.y)):
            self.x += dx
        if self.check_wall(int(self.x), int(self.y + dy * scale)):
            self.y += dy
    
    def check_sprite_collision(self, dx, dy):
        for sprite in enumerate(self.game.sprite_handler.sprite_list):
            if int(sprite[1].x) == int(self.x) and int(sprite[1].y) == int(self.y):
                if sprite[1].type == 'enemy_ammo':
                    self.increase_ammo(4)
                    self.game.sound_handler.play_sound(Sounds.AMMO)
                    self.game.sprite_handler.sprite_list.pop(sprite[0])
                    break
                if sprite[1].type == 'ammo':
                    self.increase_ammo(8)
                    self.game.sound_handler.play_sound(Sounds.AMMO)
                    self.game.sprite_handler.sprite_list.pop(sprite[0])
                    break
                if sprite[1].type == 'food':
                    self.increase_health(20)
                    self.game.sound_handler.play_sound(Sounds.FOOD)
                    self.game.sprite_handler.sprite_list.pop(sprite[0])
                    break
                if sprite[1].type == 'dog_food':
                    self.increase_health(4)
                    self.game.sound_handler.play_sound(Sounds.DOG_FOOD)
                    self.game.sprite_handler.sprite_list.pop(sprite[0])
                    break
                if sprite[1].type == 'Medkit':
                    self.increase_health(25)
                    self.game.sound_handler.play_sound(Sounds.MEDKIT)
                    self.game.sprite_handler.sprite_list.pop(sprite[0])
                    break
                if sprite[1].type == 'key_silver':
                    self.found_silver_key = True
                    self.game.sound_handler.play_sound(Sounds.KEY)
                    self.game.sprite_handler.sprite_list.pop(sprite[0])
                    break
                if sprite[1].type == 'key_golden':
                    self.found_gold_key_key = True
                    self.game.sound_handler.play_sound(Sounds.KEY)
                    self.game.sprite_handler.sprite_list.pop(sprite[0])
                    break
                if sprite[1].type == 'golden_cross':
                    self.score += 100
                    self.game.sound_handler.play_sound(Sounds.GOLDEN_CROSS)
                    self.game.sprite_handler.sprite_list.pop(sprite[0])
                    break
                if sprite[1].type == 'golden_chalice':
                    self.score += 500
                    self.game.sound_handler.play_sound(Sounds.GOLDEN_CHALICE)
                    self.game.sprite_handler.sprite_list.pop(sprite[0])
                    break
                if sprite[1].type == 'golden_chest':
                    self.score += 1000
                    self.game.sound_handler.play_sound(Sounds.GOLDEN_CHEST)
                    self.game.sprite_handler.sprite_list.pop(sprite[0])
                    break
                if sprite[1].type == 'golden_crown':
                    self.score += 5000
                    self.game.sound_handler.play_sound(Sounds.GOLDEN_CROWN)
                    self.game.sprite_handler.sprite_list.pop(sprite[0])
                    break
                if sprite[1].type == 'Rifle':
                    self.weapon_rifle = True
                    self.game.sound_handler.play_sound(Sounds.GOLDEN_CROWN)
                    self.game.sprite_handler.sprite_list.pop(sprite[0])
                    break
                if sprite[1].type == 'Minigun':
                    self.weapon_rifle = True
                    self.game.sound_handler.play_sound(Sounds.GOLDEN_CROWN)
                    self.game.sprite_handler.sprite_list.pop(sprite[0])
                    break
                if sprite[1].type == 'life_up':
                    self.lives += 1
                    self.game.sound_handler.play_sound(Sounds.PLAYER_1UP)
                    self.game.sprite_handler.sprite_list.pop(sprite[0])
                    break
            
    def increase_ammo(self, quantity):
        self.ammo += quantity
        if self.ammo > PLAYER_MAX_AMMO:
            self.ammo = PLAYER_MAX_AMMO

    def increase_health(self, quantity):
        self.health += quantity
        if self.health > PLAYER_MAX_HEALTH:
            self.health = PLAYER_MAX_HEALTH

    def mouse_control(self):
        mx, my = pg.mouse.get_pos()
        if mx < MOUSE_BORDER_LEFT or mx > MOUSE_BORDER_RIGHT:
            pg.mouse.set_pos([HALF_WIDTH, HALF_HEIGHT])
        if my < MOUSE_BORDER_TOP or my > MOUSE_BORDER_BOTTOM:
            pg.mouse.set_pos([HALF_WIDTH, HALF_HEIGHT])
        self.rel = pg.mouse.get_rel()[0]
        self.rel = max(-MOUSE_MAX_REL, min(MOUSE_MAX_REL, self.rel))
        self.angle += self.rel * MOUSE_SENSITIVITY * self.game.delta_time

    def change_weapon(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_1]:
            self.active_weapon = Weapons.KNIFE
            self.game.weapon = self.game.knife
        if keys[pg.K_2]:
            self.active_weapon = Weapons.PISTOL
            self.game.weapon = self.game.pistol
        if keys[pg.K_3] and self.weapon_rifle:
            self.active_weapon = Weapons.RIFLE
            self.game.weapon = self.game.rifle
        if keys[pg.K_4 and self.weapon_minigun]:
            self.active_weapon = Weapons.MINIGUN
            self.game.weapon = self.game.minigun    

    def draw(self):
        if IS_2D_MODEL_ENABLED:
            pg.draw.line(self.game.screen, PLAYER_ANGLE_COLOR, (self.x * MAP_RECT_SIZE, self.y * MAP_RECT_SIZE),
                        (self.x * MAP_RECT_SIZE + WIDTH * math.cos(self.angle),
                            self.y * MAP_RECT_SIZE + WIDTH * math.sin(self.angle)), 2)
        pg.draw.circle(self.game.screen, PLAYER_COLOR, (self.x * MAP_RECT_SIZE, self.y * MAP_RECT_SIZE), PLAYER_SIZE / MAP_RECT_SIZE)

    def get_starting_position(self, tmx):
        layer_data = self.game.tmx_map.get_layer_by_name('npc').data
        for row_index, row in enumerate(layer_data):
            for column_index, cell in enumerate(row):
                if cell != 0:
                    tile = self.game.tmx_map.get_tile_properties(column_index, row_index, TMX_NPC_LAYER_INDEX)
                    if tile['type'] == 'Player':
                        return column_index + 0.5, row_index + 0.5

    def get_damage(self, damage):
        self.health -= int(damage)
        if self.health < 0:
            self.health = 0
        self.game.object_renderer.player_damage()
        self.check_game_over()
        
    @property
    def position(self):
        return self.x, self.y

    @property
    def map_position(self):
        return int(self.x), int(self.y)