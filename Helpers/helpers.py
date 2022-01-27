from os import path

import pygame


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