import json
from enum import Enum

import numpy as np
import pygame

from Runtime import Runtime, Colors
from file_reader.MainMapClass import Map
from file_reader.MapConstants import HeroesConstants


def get_objects_from_json(path: str):
    with open(path, 'r') as f:
        content = f.read()
    objects_info = json.loads(content)
    objects = []
    for obj in objects_info:
        object_template = ObjectTemplate(obj['name'], obj['id'], obj['subid'], obj['tiles'], obj['pos'])
        objects.append(object_template)
    return objects


class ObjectTemplate:
    def __init__(self, name: str, idx: int, subid: int, tiles: list, pos: list[int, int, int]):
        self.name = name
        self.id = idx
        self.subid = subid
        self.tiles = np.asarray(tiles)
        self.pos = pos


class Tile:
    def __init__(self, name: str, idx: id, subid: int, pos: list[int, int, int], obstacle: bool):
        self.name = name
        self.id = idx
        self.subid = subid
        self.pos = pos

        self.tile = pygame.Rect(self.pos[0] * Runtime.tile_size[0], self.pos[1] * Runtime.tile_size[1],
                                Runtime.tile_size[0], Runtime.tile_size[1])
        self.obstacle = obstacle

        self.color = Colors.interactives_color
        if self.obstacle:
            self.color = Colors.obstacle_color
        elif "Random Monster" in self.name or self.name in HeroesConstants.Monster.values() or self.name in ["Monster"]:
            self.color = Colors.monster_color
        elif "Random Resource" in self.name or self.name in HeroesConstants.Resources.values() or self.name in ["Resource"]:
            self.color = Colors.resource_color
        elif "Random Dwelling" in self.name or self.name in ["Dwelling"]:
            self.color = Colors.dwelling_color
        elif self.name == "Water":
            self.color = Colors.water_color
        elif self.name in ["Grass", "Dirt", "Sand", "Swamp", "Snow", "Rough", "Subterranean", "Wasteland", "Highlands"]:
            self.color = Colors.terrain_color
        elif self.name == "Empty":
            self.color = Colors.undefined_tile_color

    def draw(self, window):
        pygame.draw.rect(window, self.color.value, self.tile)

    def get_info(self):
        return [f"{self.name}", f"id: {self.id}", f"subid: {self.subid}", f"obstacle: {self.obstacle}"]

    def __repr__(self):
        return self.name


class MapDataVisualApp:
    def __init__(self, path: str):
        self.path = path
        self.objects = get_objects_from_json(path)
        self.array = np.zeros((Runtime.map_size, Runtime.map_size), dtype=object)

        for obj in self.objects:
            tiles = np.asarray(obj.tiles)
            for ly, lx in np.ndindex(tiles.shape):
                position = [obj.pos[0] - lx, obj.pos[1] - ly, 0]
                if tiles[ly, lx] == 1:
                    self.array[obj.pos[0] - lx, obj.pos[1] - ly] = \
                        Tile(obj.name, obj.id, obj.subid, position, False)
                elif tiles[ly, lx] == 2:
                    self.array[obj.pos[0] - lx, obj.pos[1] - ly] = \
                        Tile(obj.name, obj.id, obj.subid, position, True)

        for y, x in np.ndindex(self.array.shape):
            if self.array[x, y] == 0:
                tile = Tile("Empty", -1, -1, [x, y, 0], False)
                self.array[x, y] = tile

    def draw(self, window):
        for y, x in np.ndindex(self.array.shape):
            self.array[y, x].draw(window)
        SelectFrame.draw(window)
        self.show_selected_info(window)

    def show_selected_info(self, window):
        if SelectFrame.selected is None:
            return
        x, y = SelectFrame.selected
        tile = self.array[x, y]
        for i, info in enumerate(tile.get_info()):
            window.blit(pygame.font.SysFont('Calibri', 18).render(info, True, (255, 255, 255)), (1200, 200+20*i))


class MapDataVisualAppVersion2:
    def __init__(self, path: str):
        new_map = Map()
        objects, terrain, road = new_map.read_map(path)
        self.objects = new_map.object_list

        self.path = path
        self.array = np.zeros((Runtime.map_size, Runtime.map_size), dtype=object)

        for obj_template in self.objects:
            obj = obj_template[0]
            more_info = obj_template[1]
            pos = obj_template[2]

            tiles = np.asarray(obj.tiles)
            for ly, lx in np.ndindex(tiles.shape):
                position = [pos[0] - lx, pos[1] - ly, 0]
                if tiles[ly, lx] == 1:
                    self.array[pos[0] - lx, pos[1] - ly] = \
                        Tile(obj.name, obj.id, obj.subid, position, False)
                elif tiles[ly, lx] == 2:
                    self.array[pos[0] - lx, pos[1] - ly] = \
                        Tile(obj.name, obj.id, obj.subid, position, True)

        for y, x in np.ndindex(self.array.shape):
            if self.array[x, y] == 0:
                terrain_type = terrain[0, y, x] if y < 72 and x < 72 else "Empty"
                tile = Tile(terrain_type, -1, -1, [x, y, 0], False)
                self.array[x, y] = tile

    def draw(self, window):
        for y, x in np.ndindex(self.array.shape):
            self.array[y, x].draw(window)
        SelectFrame.draw(window)
        self.show_selected_info(window)

    def show_selected_info(self, window):
        if SelectFrame.selected is None:
            return
        x, y = SelectFrame.selected
        tile = self.array[x, y]
        for i, info in enumerate(tile.get_info()):
            window.blit(pygame.font.SysFont('Calibri', 60, bold=True).render(info, True, (255, 255, 255)), (1000, 70+70*i))


class SelectFrame:
    selected = None

    @staticmethod
    def draw(window):
        if SelectFrame.selected is not None:
            x = SelectFrame.selected[0] * Runtime.tile_size[0]
            y = SelectFrame.selected[1] * Runtime.tile_size[1]
            SelectFrame._draw_select_frame(window, Colors.select_color.value, x, y)
            window.blit(pygame.font.SysFont('Calibri', 60, bold=True).render(
                f"SXY: {x / Runtime.tile_size[0], y / Runtime.tile_size[1]}", True, (255, 255, 255)), (1000, 370))

        mouse = pygame.mouse.get_pos()
        x, y = Runtime.round_to_grid(mouse)
        if mouse[0] > Runtime.tile_size[0] * Runtime.map_size or mouse[1] > Runtime.tile_size[1] * Runtime.map_size:
            return
        SelectFrame._draw_select_frame(window, Colors.moving_select_color.value, x, y)
        window.blit(pygame.font.SysFont('Calibri', 60, bold=True).render(
            f"XY: {x / Runtime.tile_size[0], y / Runtime.tile_size[1]}", True, (255, 255, 255)), (1000, 900))

    @staticmethod
    def select(event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse = pygame.mouse.get_pos()
            if mouse[0] > Runtime.tile_size[0] * Runtime.map_size or mouse[1] > Runtime.tile_size[1] * Runtime.map_size:
                SelectFrame.selected = None
                return

            if event.button == 1:
                x = mouse[0] // Runtime.tile_size[0]
                y = mouse[1] // Runtime.tile_size[1]
                SelectFrame.selected = None if (x, y) == SelectFrame.selected else (x, y)

    @staticmethod
    def _draw_select_frame(window, color, x, y):
        pygame.draw.line(window, color, (x, y), (x + Runtime.tile_size[0], y))
        pygame.draw.line(window, color, (x, y), (x, y + Runtime.tile_size[1]))
        pygame.draw.line(window, color, (x, y + Runtime.tile_size[1]), (x + Runtime.tile_size[0], y + Runtime.tile_size[1]))
        pygame.draw.line(window, color, (x + Runtime.tile_size[0], y), (x + Runtime.tile_size[0], y + Runtime.tile_size[1]))
