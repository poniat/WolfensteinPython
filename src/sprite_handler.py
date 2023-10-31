from typing import Any
from sprite import *
from animated_sprite import *

class SpriteHandler:
    def __init__(self, game):
        self.game = game
        self.sprite_list = []
        self.static_sprite_path = 'assets/sprites/static/'
        self.animated_sprite_path = 'assets/sprites/animated/'
        add_sprite = self.add_sprite

        #sprite map
        #starting prison
        add_sprite(Sprite(game, path=self.static_sprite_path + 'guard_dead.png', position=(30.5, 57.5)))

        add_sprite(Sprite(game, path=self.static_sprite_path + 'lamp_ceiling.png', position=(33.5, 40.5)))
        add_sprite(Sprite(game, path=self.static_sprite_path + 'lamp_ceiling.png', position=(33.5, 44.5)))
        add_sprite(AnimatedSprite(game, path='assets/sprites/npc/guard/walk/0.png', position=(33.5, 45.5), scale=1.0, shift=0.0, animation_time=120))
        add_sprite(Sprite(game, path=self.static_sprite_path + 'lamp_ceiling.png', position=(33.5, 48.5)))
        add_sprite(Sprite(game, path=self.static_sprite_path + 'lamp_ceiling.png', position=(33.5, 52.5)))
        add_sprite(Sprite(game, path=self.static_sprite_path + 'lamp_ceiling.png', position=(33.5, 52.5)))
        add_sprite(Sprite(game, path=self.static_sprite_path + 'lamp_ceiling.png', position=(33.5, 57.5)))
        add_sprite(Sprite(game, path=self.static_sprite_path + 'lamp_ceiling.png', position=(33.5, 61.5)))
        add_sprite(Sprite(game, path=self.static_sprite_path + 'lamp_ceiling.png', position=(29.5, 61.5)))
        add_sprite(Sprite(game, path=self.static_sprite_path + 'lamp_ceiling.png', position=(37.5, 61.5)))
        
        add_sprite(Sprite(game, path=self.static_sprite_path + 'food.png', position=(33.5, 62.5)))
        add_sprite(AnimatedSprite(game, path='assets/sprites/npc/guard/walk/0.png', position=(38.5, 61.5), scale=1.0, shift=0.0, animation_time=120))
        add_sprite(Sprite(game, path=self.static_sprite_path + 'ammo.png', position=(39.5, 61.5)))
        add_sprite(AnimatedSprite(game, path='assets/sprites/npc/guard/walk/0.png', position=(27.5, 62.5), scale=1.0, shift=0.0, animation_time=120))
        
        add_sprite(Sprite(game, path=self.static_sprite_path + 'food.png', position=(36.5, 57.5)))
        add_sprite(Sprite(game, path=self.static_sprite_path + 'food.png', position=(28.5, 51.5)))
        
        add_sprite(Sprite(game, path=self.static_sprite_path + 'bones2.png', position=(27.5, 51.5)))
        #add_sprite(Sprite(game, path=self.static_sprite_path + 'bones2.png', position=(39.5, 57.5)))
        add_sprite(Sprite(game, path=self.static_sprite_path + 'bones1.png', position=(37.5, 52.5)))
        
        #add_sprite(Sprite(game, path=self.static_sprite_path + 'candlebra.png', position=(37.5, 52.5), scale=0.7, shift=0.27))
        
        
        #add_sprite(AnimatedSprite(game, path=self.animated_sprite_path + 'green_light/0.png', position=(39.5, 57.5)))

    def update(self):
        [sprite.update() for sprite in self.sprite_list]

    def add_sprite(self, sprite):
        self.sprite_list.append(sprite)
        
        