from main import *
from typing import Any
from sprite import *
from animated_sprite import *
from pytmx import *


class SpriteHandler:
    def __init__(self, game: Game):
        self.game = game
        self.sprite_list = []
        self.static_sprite_path = 'assets/sprites/static/'
        self.animated_sprite_path = 'assets/sprites/animated/'
        add_sprite = self.add_sprite

        items_layer = self.game.tmx_map.get_layer_by_name('items')
        items_layer_data = items_layer.data
        tileset: TiledTileset = self.game.tmx_map.tilesets[1]  # Assuming there's only one tileset

        for row_index, row in enumerate(items_layer_data):
            for column_index, cell in enumerate(row):
                if cell != 0:
                    #tile = tileset.
                    tile = self.game.tmx_map.get_tile_properties(column_index, row_index, 2)
                    asset_path = tile['source']
                    final_path = asset_path.replace('..', 'assets')
                    add_sprite(Sprite(game, path=final_path, position=(column_index + 0.5, row_index + 0.5)))

    def update(self):
        [sprite.update() for sprite in self.sprite_list]

    def add_sprite(self, sprite):
        self.sprite_list.append(sprite)
        
        