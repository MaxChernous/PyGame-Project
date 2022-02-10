import os, pytmx

from Helpers.helpers import *


class Labyrinth:

    def __init__(self, filename, enemies):
        fullname = os.path.join(MAPS_DIR, filename)
        self.map = pytmx.load_pygame(fullname)
        self.height = self.map.height
        self.width = self.map.width
        self.tile_size = self.map.tilewidth
        self.free_tiles = FREE_TILES
        self.finish_tile = FINISH_TILE
        self.cactus_tile = CACTUS_TILE
        self.enemies = enemies

    def render(self, screen):
        for y in range(self.height):
            for x in range(self.width):
                image = self.map.get_tile_image(x, y, 0)
                screen.blit(image, (x * self.tile_size, y * self.tile_size))

    def get_tile_id(self, position):
        return self.map.tiledgidmap[self.map.get_tile_gid(*position, 0)]

    def is_free(self, position, for_hero=True):
        if for_hero:
            return self.get_tile_id(position) in self.free_tiles
        else:
            return self.get_tile_id(position) in self.free_tiles and \
                   self.get_tile_id(position) != self.cactus_tile

    def find_path_step(self, start, target):
        INF = 10000
        x, y = start
        distance = [[INF] * self.width for _ in range(self.height)]
        distance[y][x] = 0
        prev = [[None] * self.width for _ in range(self.height)]
        queue = [(x, y)]
        while queue:
            x, y = queue.pop(0)
            for dx, dy in (1, 0), (0, 1), (-1, 0), (0, -1):
                next_x, next_y = x + dx, y + dy
                if 0 <= next_x < self.width and 0 < next_y < self.height and \
                        self.is_free((next_x, next_y), False) and distance[next_y][next_x] == INF:
                    distance[next_y][next_x] = distance[y][x] + 1
                    prev[next_y][next_x] = (x, y)
                    queue.append((next_x, next_y))
        x, y = target
        if distance[y][x] == INF or start == target:
            return start
        while prev[y][x] != start:
            x, y = prev[y][x]

        free = True
        for enemy in self.enemies:
            if enemy.get_position() == (x, y) and enemy.life:
                free = False
        if free:
            return x, y
        else:
            return start
