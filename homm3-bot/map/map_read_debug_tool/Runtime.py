from enum import Enum

import pygame


class Colors(Enum):
    obstacle_color = (255, 0, 0)  # RED
    monster_color = (0, 0, 0)  # BLACK
    resource_color = (225, 180, 0)  # GOLD
    interactives_color = (0, 0, 255)  # BLUE
    dwelling_color = (0, 255, 0)  # GREEN
    undefined_tile_color = (255, 255, 255)  # WHITE
    water_color = (100, 100, 255)  # LIGHT BLUE
    terrain_color = (100, 255, 100)  # LIGHT GREEN

    moving_select_color = (80, 80, 80)  # GRAY
    select_color = (40, 40, 40)  # GRAY


class Runtime:
    tile_size = (12, 12)
    map_size = 80

    @staticmethod
    def round_to_grid(coord: tuple[int, int]):
        x = coord[0] // Runtime.tile_size[0] * Runtime.tile_size[0]
        y = coord[1] // Runtime.tile_size[1] * Runtime.tile_size[1]
        return x, y
