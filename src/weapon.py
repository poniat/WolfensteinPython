from animated_sprite import *

class Weapon(AnimatedSprite):
    def __init__(self, game, type, path='assets/sprites/weapon/pistol/0.png',
                 scale=GAME_SCALE * 2,
                 animation_time=100):
        super().__init__(game=game, type=type, path=path, scale=scale, animation_time=animation_time)
        self.images = deque(
            [pg.transform.scale(img, (self.image.get_width() * scale, self.image.get_height() * scale))
             for img in self.images])
        self.weapon_pos = (HALF_WIDTH - self.images[0].get_width() // 2, HEIGHT - self.images[0].get_height() - self.game.object_renderer.hud_background_image.get_height())
        self.is_reloading = False
        self.num_images = len(self.images)
        self.frame_counter = 0
        self.damage = 50

    def animate_shot(self):
        if self.is_reloading:
            self.game.player.shot = False
            if self.animation_trigger:
                self.images.rotate(-1)
                self.image = self.images[0]
                self.frame_counter += 1
                if self.frame_counter == self.num_images:
                    self.is_reloading = False
                    self.frame_counter = 0

    def update(self):
        self.game.screen.blit(self.images[0], self.weapon_pos)
    
    def draw(self):        
        self.check_animation_time()
        self.animate_shot()
        
class Knife(Weapon):
    def __init__(self, game, type, path='assets/sprites/weapon/knife/0.png'):
        super().__init__(game=game, type=type, path=path, scale=GAME_SCALE * 2, animation_time=80)

class Rifle(Weapon):
    def __init__(self, game, type, path='assets/sprites/weapon/rifle/0.png'):
        super().__init__(game=game, type=type, path=path, scale=GAME_SCALE * 2, animation_time=35)

class Minigun(Weapon):
    def __init__(self, game, type, path='assets/sprites/weapon/minigun/0.png'):
        super().__init__(game=game, type=type, path=path, scale=GAME_SCALE * 2, animation_time=15)