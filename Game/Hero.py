import pygame

from Entities.Player import Player
from Helpers.Bombs import TILE_SIZE


class Hero(Player):
    #    sword_image = load_image("hero_sword_image.png")
    #    pistol_image = load_image("hero_pistol_image.png")
    #    rifle_image = load_image("hero_rifle_image.png")

    INTERVAL = 120  # milliseconds between animation frame
    OFFSET_X = TILE_SIZE / 1.5
    OFFSET_Y = TILE_SIZE / 1.5 + 5

    def __init__(self, picture, columns, rows, *groups, rect=None, speed=2, weapon, stages=None):
        if not rect:
            rect = pygame.Rect(0, 0, picture.get_width() // columns, picture.get_height() // rows)
        self.rect = rect
        self.speed = speed
        self.time = pygame.time.Clock()
        self.timer = 0
        self.x_dir = 0
        self.y_dir = 0
        self.weapon = weapon
        self.x = rect.x
        self.y = rect.y

        super(Hero, self).__init__(picture, columns, rows, *groups, rect=rect, stages=stages)

        self.stage = "Idle"

    def get_position(self):
        return self.x, self.y

    def set_position(self, position):
        self.x, self.y = position

    def update(self, screen):
        super().update()

        self.image = pygame.transform.scale(self.image, (TILE_SIZE * 2.5, TILE_SIZE * 2.5))
        self.rect.x = self.x * TILE_SIZE - self.OFFSET_X
        self.rect.y = self.y * TILE_SIZE - self.OFFSET_Y
        self.mask = pygame.mask.from_surface(self.image)
