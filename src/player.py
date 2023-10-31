from settings import *
import pygame as pg
import math
from sound_handler import *

class Player:
    def __init__(self, game):
        self.game = game
        self.x, self.y = PLAYER_START_POSITION
        self.angle = PLAYER_ANGLE
        self.shot = False

    def single_fire_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1 and not self.shot and not self.game.weapon.is_reloading:
                self.game.sound_handler.play_sound(Sounds.PLAYER_PISTOL)
                self.shot = True
                self.game.weapon.is_reloading = True


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

        if keys[pg.K_LEFT]:
            self.angle -= PLAYER_ROTATION_SPEED * self.game.delta_time
        if keys[pg.K_RIGHT]:
            self.angle += PLAYER_ROTATION_SPEED * self.game.delta_time
        self.angle %= math.tau

    def check_wall(self, x, y):
        return (x, y) not in self.game.map.world_map

    def check_wall_collision(self, dx, dy):
        scale = PLAYER_SIZE_SCALE / self.game.delta_time
        if self.check_wall(int(self.x + dx * scale), int(self.y)):
            self.x += dx
        if self.check_wall(int(self.x), int(self.y + dy * scale)):
            self.y += dy
    
    def mouse_control(self):
        mx, my = pg.mouse.get_pos()
        if mx < MOUSE_BORDER_LEFT or mx > MOUSE_BORDER_RIGHT:
            pg.mouse.set_pos([HALF_WIDTH, HALF_HEIGHT])
        self.rel = pg.mouse.get_rel()[0]
        self.rel = max(-MOUSE_MAX_REL, min(MOUSE_MAX_REL, self.rel))
        self.angle += self.rel * MOUSE_SENSITIVITY * self.game.delta_time

    def update(self):
        self.movement()
        self.mouse_control()

    def draw(self):
        # pg.draw.line(self.game.screen, PLAYER_ANGLE_COLOR, (self.x * MAP_RECT_SIZE, self.y * MAP_RECT_SIZE),
        #               (self.x * MAP_RECT_SIZE + WIDTH * math.cos(self.angle),
        #                self.y * MAP_RECT_SIZE + WIDTH * math.sin(self.angle)), 2)
        pg.draw.circle(self.game.screen, PLAYER_COLOR, (self.x * MAP_RECT_SIZE, self.y * MAP_RECT_SIZE), PLAYER_SIZE)

    @property
    def position(self):
        return self.x, self.y

    @property
    def map_position(self):
        return int(self.x), int(self.y)