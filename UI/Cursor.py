from typing import Any

import pygame


class Cursor(pygame.sprite.Sprite):
    def __init__(self, image: pygame.surface.Surface, *group: pygame.sprite.AbstractGroup):
        super().__init__(*group)
        self.image = image
        self.rect: pygame.rect.Rect = self.image.get_rect()

    def update(self, *args: "list[Any]"):
        if pygame.mouse.get_focused():
            self.rect.x, self.rect.y = args[0][0], args[0][1]
        else:
            self.remove()