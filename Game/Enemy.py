import pygame

from Helpers.helpers import ENEMY_EVENT_TYPE, TILE_SIZE, load_image


class Enemy(pygame.sprite.Sprite):
    life_image = load_image("enemy_life_image.png")
    dead_image = load_image("enemy_dead_image.png")

    def __init__(self, group, position, delay, radius_trigger):
        super().__init__(group)
        self.image = Enemy.life_image
        self.image = pygame.transform.scale(self.image, (TILE_SIZE, TILE_SIZE))
        self.rect = self.image.get_rect()
        self.x, self.y = position
        self.rect.x = self.x * TILE_SIZE
        self.rect.y = self.y * TILE_SIZE
        self.delay = delay
        pygame.time.set_timer(ENEMY_EVENT_TYPE, self.delay)
        self.life = True
        self.triggered = False
        self.radius_trigger = radius_trigger
        self.mask = pygame.mask.from_surface(self.image)

    def get_position(self):
        return self.x, self.y

    def set_position(self, position):
        self.x, self.y = position

    def update(self, screen):
        if self.life:
            self.image = Enemy.life_image
        else:
            self.image = Enemy.dead_image

        self.image = pygame.transform.scale(self.image, (TILE_SIZE, TILE_SIZE))
        self.rect.x = self.x * TILE_SIZE
        self.rect.y = self.y * TILE_SIZE
        self.mask = pygame.mask.from_surface(self.image)
