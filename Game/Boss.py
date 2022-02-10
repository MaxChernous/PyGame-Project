import pygame

from Helpers.helpers import TILE_SIZE, BOSS_EVENT_TYPE, BOSS_DELAY, load_image


class Boss(pygame.sprite.Sprite):
    life_image = load_image("boss_life_image.png")
    dead_image = load_image("boss_dead_image.png")

    def __init__(self, group, position):
        super().__init__(group)
        self.image = Boss.life_image
        self.image = pygame.transform.scale(self.image, (TILE_SIZE * 4, TILE_SIZE * 3))
        self.rect = self.image.get_rect()
        self.x, self.y = position
        self.rect.x = self.x * TILE_SIZE
        self.rect.y = self.y * TILE_SIZE
        pygame.time.set_timer(BOSS_EVENT_TYPE, BOSS_DELAY)
        self.health_points = 30
        self.mask = pygame.mask.from_surface(self.image)

    def damage(self):
        self.health_points -= 1

    def update(self, screen):
        if self.health_points > 0:
            self.image = Boss.life_image
        else:
            self.image = Boss.dead_image

        self.image = pygame.transform.scale(self.image, (TILE_SIZE * 4, TILE_SIZE * 3))
        self.rect.x = self.x * TILE_SIZE
        self.rect.y = self.y * TILE_SIZE
        self.mask = pygame.mask.from_surface(self.image)
