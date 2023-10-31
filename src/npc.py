from animated_sprite import *
from random import randint, random, choice
from sound_handler import *

class Npc(AnimatedSprite):
    def __init__(self, game, path='assets/sprites/npc/guard/0.png',
                 pos=(35.5, 61.5),
                 scale=0.8,
                 shift=0.2,
                 animation_time=180):
        super().__init__(game, path, pos, scale, shift, animation_time)
        self.attack_images = self.get_images(self.path + '/attack')
        self.death_images = self.get_images(self.path + '/death')
        self.idle_images = self.get_images(self.path + '/idle')
        self.pain_images = self.get_images(self.path + '/pain')
        self.walk_images = self.get_images(self.path + '/walk')

        self.attack_distance = randint(3, 6)
        self.speed = 0.03
        self.size = 10
        self.health = 100
        self.attack_damage = 10
        self.attack_accuracy = 0.15
        self.alive = True
        self.pain = False
        self.frame_counter = 0

        self.is_line_of_sight_to_player = False

    def run_logic(self):
        if self.alive:
            self.is_line_of_sight_to_player = self.raycast_line_of_sight_npc_to_player()
            self.check_if_hit_by_player()
            if self.pain:
                self.animate_pain()
            elif self.is_line_of_sight_to_player:
                self.animate(self.walk_images)
                self.movement()
            else:
                self.animate(self.idle_images)
        else:
            self.animate_death()

    def update(self):
        self.check_animation_time()
        self.get_sprite()
        self.run_logic()
        self.draw_ray_cast()

    def movement(self):
        next_pos = self.game.player.map_position
        next_x, next_y = next_pos
        angle = math.atan2(next_y + 0.5 - self.y, next_x + 0.5 - self.x)
        dx = math.cos(angle) * self.speed
        dy = math.sin(angle) * self.speed
        self.check_wall_collision(dx, dy)

    def check_wall(self, x, y):
        return (x, y) not in self.game.map.world_map

    def check_wall_collision(self, dx, dy):
        if self.check_wall(int(self.x + dx * self.size), int(self.y)):
            self.x += dx
        if self.check_wall(int(self.x), int(self.y + dy * self.size)):
            self.y += dy

    def animate_death(self):
        if not self.alive:
            if self.animation_trigger and self.frame_counter < len(self.death_images) - 1:
                self.death_images.rotate(-1)
                self.image = self.death_images[0]
                self.frame_counter += 1
        
    def animate_pain(self):
        self.animate(self.pain_images)
        if self.animation_trigger:
            self.pain = False

    def check_if_hit_by_player(self):
        if self.is_line_of_sight_to_player and self.game.player.shot:
            if HALF_WIDTH - self.sprite_half_width < self.screen_x < HALF_WIDTH + self.sprite_half_width:
                self.game.sound_handler.play_sound(Sounds.NPC_PAIN)
                self.game.player.shot = False
                self.pain = True
                self.health -= self.game.weapon.damage
                self.check_health()

    def check_health(self):
        if self.health < 1:
            self.alive = False
            self.game.sound_handler.play_sound(Sounds.NPC_DEATH)

    @property
    def map_pos(self):
        return int(self.x), int(self.y)
    
    def raycast_line_of_sight_npc_to_player(self):
        if self.game.player.map_position == self.map_pos:
            return True

        wall_dist_v, wall_dist_h = 0, 0
        player_dist_v, player_dist_h = 0, 0

        player_x, player_y = self.game.player.position
        map_x, map_y = self.game.player.map_position
                
        ray_angle = self.theta
        
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
            if tile_hor == self.map_pos:
                player_dist_h = depth_hor
                break
            if tile_hor in self.game.map.world_map:
                wall_dist_h = depth_hor
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
            if tile_vert == self.map_pos:
                player_dist_v = depth_vert
                break
            if(tile_vert in self.game.map.world_map):
                wall_dist_v = depth_vert
                break

            x_vert += dx
            y_vert += dy
            depth_vert += delta_depth

        player_dist = max(player_dist_v, player_dist_h)
        wall_dist = max(wall_dist_v, wall_dist_h)

        if 0 < player_dist < wall_dist or not wall_dist:
            return True
        return False
    
    def draw_ray_cast(self):
        if IS_2D_MODEL_ENABLED:
            pg.draw.circle(self.game.screen, 'red', (MAP_RECT_SIZE * self.x, MAP_RECT_SIZE * self.y), self.size)
            if self.raycast_line_of_sight_npc_to_player():
                pg.draw.line(self.game.screen, 'orange', (MAP_RECT_SIZE * self.game.player.x, MAP_RECT_SIZE * self.game.player.y),
                            (MAP_RECT_SIZE * self.x, MAP_RECT_SIZE * self.y), 2)

    
