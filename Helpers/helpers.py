from os import path

import pygame

SIZE = WIDTH, HEIGHT = 672, 608
TILE_SIZE = 32
FPS = 15
MAPS_DIR = "maps"

FREE_TILES = [30, 31, 39, 40, 46]
FINISH_TILE = 46
NEW_WEAPON_TILE = 39
CACTUS_TILE = 31

ENEMY_EVENT_TYPE = 30
BOSS_EVENT_TYPE = 40
STOPWATCH_EVENT_TYPE = 50

BOSS_DELAY = 2000
STOPWATCH_DELAY = 1000

PISTOL_SPRITE = 39


def load_image(name: str):
    '''
    Load an image file and return it.
    
    :param name: The name of the image file to load
    :type name: str
    :return: A list of images.
    '''
    fullname = path.join('data', name)
    if not path.isfile(fullname):
        print(f"Image file '{fullname}' not found")
        exit()
    image = pygame.image.load(fullname)
    return image
