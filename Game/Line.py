import pygame

from Helpers.helpers import SIZE


class Line(pygame.sprite.Sprite):
    def __init__(self, group, screen, from_pos, to_pos):
        super().__init__(group)
        self.image = pygame.Surface(SIZE)
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0
        self.screen = screen

        self.from_pos = from_pos
        self.to_pos = to_pos
        self.dx = to_pos[0] - self.from_pos[0]
        self.dy = to_pos[1] - self.from_pos[1]
        pygame.draw.line(self.image, (0, 200, 0), self.from_pos, (to_pos[0] + self.dx * 1000,
                                                                  self.to_pos[1] + self.dy * 1000), 20)
        self.mask = pygame.mask.from_surface(self.image)

        self.updates_count = 0

    def update(self, screen):
        self.updates_count += 1
        if self.updates_count > 3:
            self.kill()
