import os
import sys
import pygame


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)

    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class Cursor(pygame.sprite.Sprite):
    def __init__(self, *group):
        super().__init__(*group)
        self.image = pygame.transform.scale(load_image("cursor.png"), (50, 50))
        self.rect = self.image.get_rect()

    def update(self, *args):
        if pygame.mouse.get_focused():
            self.rect.x, self.rect.y = args[0][0], args[0][1]
        else:
            self.remove()


if __name__ == '__main__':
    pygame.init()
    size = width, height = 300, 300
    screen = pygame.display.set_mode(size)
    running = True
    all_sprites = pygame.sprite.Group()
    cur = Cursor(all_sprites)
    pygame.mouse.set_visible(False)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEMOTION:
                all_sprites.update(event.pos)

        screen.fill('black')
        if pygame.mouse.get_focused():
            all_sprites.draw(screen)
        pygame.display.flip()
    pygame.quit()
