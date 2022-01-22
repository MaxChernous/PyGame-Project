import pygame


class Cursor(pygame.sprite.Sprite):
    def __init__(self, image, *group):
        super().__init__(*group)
        self.image = image
        self.rect = self.image.get_rect()

    def update(self, *args):
        if pygame.mouse.get_focused():
            self.rect.x, self.rect.y = args[0][0], args[0][1]
        else:
            self.remove()