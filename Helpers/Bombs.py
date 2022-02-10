import pygame

from Helpers.helpers import load_image

TILE_SIZE = 32


class Bomb(pygame.sprite.Sprite):
    image = load_image("bomb.png")
    image_boom = load_image("boom.png")

    def __init__(self, position, *group):
        super().__init__(*group)
        self.image = Bomb.image
        self.rect = self.image.get_rect()
        self.x, self.y = position
        self.rect.x = self.x * TILE_SIZE
        self.rect.y = self.y * TILE_SIZE
        self.updates_count = 0
        self.stage = "bomb"

    def update(self, screen):
        self.updates_count += 1
        if self.updates_count == 9:
            self.image = Bomb.image_boom
        elif self.updates_count == 15:
            self.kill()
