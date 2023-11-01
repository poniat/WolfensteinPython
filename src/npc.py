from animated_sprite import *
from random import randint, random, choice
from sound_handler import *
from main import *

class Npc(AnimatedSprite):
    def __init__(self, game, type, path='assets/sprites/npc/guard/0.png',
                 pos=(35.5, 61.5),
                 scale=1.0,
                 shift=0.0,
                 animation_time=200):
        super().__init__(game, type, path, pos, scale, shift, animation_time)
        self.attack_images = self.get_images(self.path + '/attack')
        self.death_images = self.get_images(self.path + '/death')
        self.idle_images = self.get_images(self.path + '/idle')
        self.pain_images = self.get_images(self.path + '/pain')
        self.walk_images = self.get_images(self.path + '/walk')

        self.shot = False
        self.is_reloading = False
        self.idle = True
        self.attack_distance = randint(3, 6)
        self.speed = 0.03
        self.size = 70
        self.health = 25
        self.kill_score = 100
        self.attack_damage = 10
        self.attack_accuracy = 0.15
        self.alive = True
        self.pain = False
        self.attack_frame_counter = 0
        self.death_frame_counter = 0
        self.shots_fired = 0

        self.is_line_of_sight_to_player = False

    def run_logic(self):
        if self.alive:
            self.is_line_of_sight_to_player = self.raycast_line_of_sight_npc_to_player()
            self.check_if_hit_by_player()
            if self.pain:
                self.animate_pain()
            elif self.is_line_of_sight_to_player:
                self.check_idle()
                if self.dist < self.attack_distance:
                    self.animate(self.attack_images)
                    self.attack_player()
                    if self.is_reloading:
                        self.shot = False
                        if self.animation_trigger:
                            self.attack_frame_counter += 1
                            if self.attack_frame_counter == len(self.attack_images):
                                self.is_reloading = False
                                self.attack_frame_counter = 0
                else:
                    self.animate(self.walk_images)
                    self.movement()
            else:
                self.animate(self.idle_images)
        else:
            self.animate_death()


    def check_idle(self):
        if self.idle:
            rand = randint(1, 100)
            if rand < 2:
                self.game.sound_handler.play_sound(Sounds.NPC_TALK_KOMM_HIER_SCHWEIN)
            elif rand < 5:
                self.game.sound_handler.play_sound(Sounds.NPC_TALK_SCHUTZ_STAFFEL)
            elif rand < 10:
                self.game.sound_handler.play_sound(Sounds.NPC_TALK_GUTEN_TAG)
        self.idle = False

    def is_player_hit(self):
        #A random number between 0 and 255 (inclusive). Used for hit calculation.
        rand1 = randint(0, 255)
        
        #Distance between enemy and player (in number of squares).
        dist = self.dist

        #160 (if player is running)
        #256 (if player isn't)
        speed = 160

        #16 (if player can see the shooter)
        #8 (if the player can’t).
        look = 16

        #Player is considered hit if: [RAND1] < ( [SPEED] - ( [DIST] x [LOOK] ) )
        print('Shot nr :' + str(self.shots_fired) + '. Hit: ' + str(rand1 < (speed - (dist * look))))
        return rand1 < (speed - (dist * look))

    
    def attack_player(self):
        if not self.shot and not self.is_reloading:
            self.game.sound_handler.play_sound(Sounds.PLAYER_PISTOL)
            self.shot = True
            self.shots_fired += 1
            self.is_reloading = True
            if self.is_player_hit():
                # If shooter is SS or Boss then: [DIST] = [DIST] x (2 / 3)
                # If ( [DIST] less than 2 ) then damage is: [RAND2] / 4
                damage = 0
                rand2 = randint(0, 255)
                if self.dist < 2:
                    damage = rand2 / 4
                # If ( [DIST] between 2 and 4 ) then damage is: [RAND2] / 8
                elif self.dist >= 2 and self.dist < 4:
                    damage = rand2 / 8
                # If ( [DIST] is 4 or more ) then damage is: [RAND2] / 16
                elif self.dist >= 4:
                    damage = rand2 / 16

                if GAME_DIFFICULTY == Difficulty.EASY_CAN_I_PLAY_DADDY:
                    damage /= 2
                elif GAME_DIFFICULTY == Difficulty.HARD_BRING_EM_ON:
                    damage *= 2
                elif GAME_DIFFICULTY == Difficulty.IMPOSSIBLE_IAM_DEATH_INCARNATE:
                    damage *= 4

                print('Damage to player: ' + str(int(damage)))

                if damage > 0:
                    self.player.get_damage(damage)

            

            # If “Can I play daddy” then [DAMAGE] = [DAMAGE] / 4

            # if self.dist >= 4 and randint(0, 255) / 12 < self.dist:
            #     damage = randint(0, 255) / 6
            #     self.player.get_damage(damage)
            # elif self.dist < 2:
            #     damage = randint(0, 255) / 4
            #     self.player.get_damage(damage)
            # elif self.dist >= 2:
            #     damage = randint(0, 255) / 6
            #     self.player.get_damage(damage)


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
            if self.animation_trigger and self.death_frame_counter < len(self.death_images) - 1:
                self.death_images.rotate(-1)
                self.image = self.death_images[0]
                self.death_frame_counter += 1
        
    def animate_pain(self):
        self.animate(self.pain_images)
        if self.animation_trigger:
            self.pain = False

    def check_if_hit_by_player(self):
        if self.is_line_of_sight_to_player and self.game.player.shot:
            if HALF_WIDTH - self.sprite_half_width < self.screen_x < HALF_WIDTH + self.sprite_half_width:
                rand1 = randint(0, 255)
                if self.dist >= 4 and not rand1 / 12 < self.dist:
                    return                                  
                self.game.player.shot = False
                self.game.sound_handler.play_sound(Sounds.NPC_PAIN)
                self.pain = True
                self.health -= self.calculate_damage_to_npc()
                self.check_health()

    def calculate_damage_to_npc(self):
        damage = 0
        if self.game.player.active_weapon == Weapons.KNIFE:
            rand2 = randint(0, 255)
            damage = rand2 / 16
        if self.dist >= 2:
            rand2 = randint(0, 255)
            damage = rand2 / 6
        else:
            rand2 = randint(0, 255)
            damage = rand2 / 4
        return damage


    def check_health(self):
        if self.health < 1:
            self.alive = False
            self.game.player.score += self.kill_score
            self.die()

    def die(self):
        self.game.sound_handler.play_sound(Sounds.NPC_GUARD_DEATH)
        self.game.sprite_handler.add_sprite(Sprite(self.game, type='enemy_ammo', path='assets/sprites/static/ammo.png', position=(self.x, self.y)))

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

        self.player_dist = max(player_dist_v, player_dist_h)
        wall_dist = max(wall_dist_v, wall_dist_h)

        if 0 < self.player_dist < wall_dist or not wall_dist:
            return True
        return False
    
    def draw_ray_cast(self):
        if IS_2D_MODEL_ENABLED or self.game.is_minimap_visible:
            pg.draw.circle(self.game.screen, 'red', (MAP_RECT_SIZE * self.x, MAP_RECT_SIZE * self.y), self.size / MAP_RECT_SIZE)
            if self.raycast_line_of_sight_npc_to_player():
                pg.draw.line(self.game.screen, 'orange', (MAP_RECT_SIZE * self.game.player.x, MAP_RECT_SIZE * self.game.player.y),
                            (MAP_RECT_SIZE * self.x, MAP_RECT_SIZE * self.y), 2)

    
class Dog(Npc):
    def __init__(self, game, type, path='assets/sprites/npc/dog/0.png',
                 pos=(35.5, 61.5),
                 scale=1.0,
                 shift=0.0,
                 animation_time=200):
        super().__init__(game, type, path, pos, scale, shift, animation_time)
              
        self.attack_distance = 2
        self.speed = 0.04
        self.size = 10
        self.health = 1
        self.kill_score = 200
        self.attack_damage = 10
        self.attack_accuracy = 0.15

    def die(self):
        self.game.sound_handler.play_sound(Sounds.NPC_DOG_DEATH)

class SS(Npc):
    def __init__(self, game, type, path='assets/sprites/npc/ss/0.png',
                 pos=(35.5, 61.5),
                 scale=1.0,
                 shift=0.0,
                 animation_time=200):
        super().__init__(game, type, path, pos, scale, shift, animation_time)
              
        self.attack_distance = randint(2, 8)
        self.speed = 0.05
        self.size = 15
        self.health = 100
        self.kill_score = 500
        self.attack_damage = randint(1, 15)
        self.attack_accuracy = 0.15

    

#damage, score, hp
#https://wl6.fandom.com/wiki/Category:Enemies