import pygame as pg
import math
from settings import *

class RayCasting:
    def __init__(self, game):
        self.game = game
        self.ray_casting_result = []
        self.objects_to_render = []
        self.wall_textures = self.game.object_renderer.wall_textures

    def get_objects_to_render(self):
        self.objects_to_render = []
        for ray, values in enumerate(self.ray_casting_result):
            depth, proj_height, texture, offset = values

            if proj_height < HEIGHT:
                wall_column = self.wall_textures[texture].subsurface(
                    offset * (TEXTURE_SIZE - SCALE), 0, SCALE, TEXTURE_SIZE
                )
                wall_column = pg.transform.scale(wall_column, (SCALE, proj_height))
                wall_pos = (ray * SCALE, HALF_HEIGHT - proj_height // 2)
            else:
                texture_height = TEXTURE_SIZE * HEIGHT / proj_height
                wall_column = self.wall_textures[texture].subsurface(
                    offset * (TEXTURE_SIZE - SCALE), HALF_TEXTURE_SIZE - texture_height // 2,
                    SCALE, texture_height
                )
                wall_column = pg.transform.scale(wall_column, (SCALE, HEIGHT))
                wall_pos = (ray * SCALE, 0)

            self.objects_to_render.append((depth, wall_column, wall_pos))

    def ray_cast(self):
        self.ray_casting_result = []
        player_x, player_y = self.game.player.position
        map_x, map_y = self.game.player.map_position

        texture_vert, texture_hor = 1, 1
                
        ray_angle = self.game.player.angle - HALF_FIELD_OF_VIEW + 0.0001
        for ray in range(NUMBER_OF_RAYS):
            sin_angle = math.sin(ray_angle)
            cos_angle = math.cos(ray_angle)


            #horizontals
            y_hor, dy = (map_y + 1, 1) if sin_angle > 0 else (map_y - 1e-6, -1)

            depth_hor = (y_hor - player_y) / sin_angle
            x_hor = player_x + depth_hor * cos_angle

            delta_depth = dy / sin_angle
            dx = delta_depth * cos_angle

            for i in range(MAX_DEPTH):
                tile_hor = int(x_hor), int(y_hor)
                if tile_hor in self.game.map.world_map:
                    texture_hor = self.game.map.world_map[tile_hor]
                    break

                x_hor += dx
                y_hor += dy
                depth_hor += delta_depth

            #verticals
            x_vert, dx = (map_x + 1, 1) if cos_angle > 0 else (map_x - 1e-6, -1)

            depth_vert = (x_vert - player_x) / cos_angle
            y_vert = player_y + depth_vert * sin_angle

            delta_depth = dx / cos_angle
            dy = delta_depth * sin_angle

            for i in range(MAX_DEPTH):
                tile_vert = int(x_vert), int(y_vert)
                if(tile_vert in self.game.map.world_map):
                    texture_vert = self.game.map.world_map[tile_vert]
                    break

                x_vert += dx
                y_vert += dy
                depth_vert += delta_depth
            
            

            #depth, texture offset
            if depth_vert < depth_hor:
                depth, texture = depth_vert, texture_vert
                y_vert %= 1
                offset = y_vert if cos_angle > 0 else (1 - y_vert)
            else:
                depth, texture = depth_hor, texture_hor
                x_hor %= 1
                offset = (1 - x_hor) if sin_angle > 0 else x_hor
            
            #test draw
            #pg.draw.line(self.game.screen, 'yellow', (MAP_RECT_SIZE * player_x, MAP_RECT_SIZE * player_y),
            #              (MAP_RECT_SIZE * player_x + MAP_RECT_SIZE * depth * cos_angle, MAP_RECT_SIZE * player_y + MAP_RECT_SIZE * depth * sin_angle), 2)

            #remove fishbowl effect
            depth *= math.cos(self.game.player.angle - ray_angle)

            #projection
            proj_height = SCREEN_DISTANCE_TO_PLAYER / (depth + 0.0001)

            #draw walls as solid color
            #color = [200 / (1 + depth ** 5 * 0.00002)] * 3
            #pg.draw.rect(self.game.screen, color, (ray * SCALE, HALF_HEIGHT - proj_height // 2, SCALE, proj_height))

            #draw walls with wall_textures
            self.ray_casting_result.append((depth, proj_height, texture, offset))

            ray_angle += DELTA_ANGLE

    def update(self):
        self.ray_cast()
        self.get_objects_to_render()

