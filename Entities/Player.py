from os import path

import pygame

from AnimatedSprite import AnimatedSprite


class Player(AnimatedSprite):
    INTERVAL = 70  # milliseconds between animation frame

    def __init__(self, picture, columns, rows, *groups, rect=None, speed=1):
        if not rect:
            rect = pygame.Rect(0, 0, picture.get_width() // columns, picture.get_height() // rows)
        self.rect = rect
        self.speed = speed
        self.time = pygame.time.Clock()
        self.timer = 0
        self.x_dir = 0
        self.y_dir = 0

        super(Player, self).__init__(picture, columns, rows, rect.x, rect.y, *groups)

    def update(self, event=None):
        self.timer += self.time.tick()
        if self.timer >= self.INTERVAL:
            self.timer = 0
            super().update()
        if event:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    self.y_dir = -1
                if event.key == pygame.K_a:
                    self.x_dir = -1
                if event.key == pygame.K_s:
                    self.y_dir = 1
                if event.key == pygame.K_d:
                    self.x_dir = 1
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    self.y_dir = 0
                if event.key == pygame.K_a:
                    self.x_dir = 0
                if event.key == pygame.K_s:
                    self.y_dir = 0
                if event.key == pygame.K_d:
                    self.x_dir = 0
        self.move()

    def move(self):
        self.rect.x += self.speed * self.x_dir
        self.rect.y += self.speed * self.y_dir


def load_image(name):
    fullname = path.join(*name)
    if not path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        exit()
    image = pygame.image.load(fullname)
    return image


if __name__ == '__main__':
    pygame.init()
    size = width, height = 1350, 825
    fps = 300
    clock = pygame.time.Clock()
    all_sprites = pygame.sprite.Group()
    animated_sprites = pygame.sprite.Group()
    screen = pygame.display.set_mode(size)
    Player(load_image(["..", "data", "player.png"]), 5, 2, all_sprites, animated_sprites)
    running = True

    while running:
        screen.fill('black')
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            all_sprites.update(event)
        all_sprites.draw(screen)
        animated_sprites.update()
        clock.tick(fps)
        pygame.display.flip()
    pygame.quit()
