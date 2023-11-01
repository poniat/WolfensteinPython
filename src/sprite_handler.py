from main import *
from typing import Any
from sprite import *
from animated_sprite import *
from pytmx import *
from npc import *


class SpriteHandler:
    def __init__(self, game):
        self.game = game
        self.sprite_list = []
        self.npc_list = []
        self.npc_sprite_path = 'assets/sprites/npc/'
        self.static_sprite_path = 'assets/sprites/static/'
        self.animated_sprite_path = 'assets/sprites/animated/'
        add_sprite = self.add_sprite
        add_npc = self.add_npc

        #load items and objects
        items_layer = self.game.tmx_map.get_layer_by_name('items')
        items_layer_data = items_layer.data

        for row_index, row in enumerate(items_layer_data):
            for column_index, cell in enumerate(row):
                if cell != 0:
                    tile = self.game.tmx_map.get_tile_properties(column_index, row_index, TMX_ITEMS_LAYER_INDEX)
                    asset_path = tile['source']
                    final_path = asset_path.replace('..', 'assets')
                    add_sprite(Sprite(game, path=final_path, position=(column_index + 0.5, row_index + 0.5)))

        #load NPCs
        npc_layer = self.game.tmx_map.get_layer_by_name('npc')
        npc_layer_data = npc_layer.data

        for row_index, row in enumerate(npc_layer_data):
            for column_index, cell in enumerate(row):
                if cell != 0:
                    tile = self.game.tmx_map.get_tile_properties(column_index, row_index, TMX_NPC_LAYER_INDEX)
                    if tile['type'] == 'Guard':
                        add_npc(Npc(game, pos=(column_index + 0.5, row_index + 0.5)))
                    elif tile['type'] == 'Dog':
                        add_npc(Dog(game, pos=(column_index + 0.5, row_index + 0.5)))

    def update(self):
        [sprite.update() for sprite in self.sprite_list]
        [npc.update() for npc in self.npc_list]

    def add_sprite(self, sprite):
        self.sprite_list.append(sprite)
    
    def add_npc(self, npc):
        self.npc_list.append(npc)
        
        