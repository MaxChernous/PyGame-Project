from os import path

import pygame


def load_image(name: str):
    fullname = path.join('data', name)
    if not path.isfile(fullname):
        print(f"Image file '{fullname}' not found")
        exit()
    image = pygame.image.load(fullname)
    return image