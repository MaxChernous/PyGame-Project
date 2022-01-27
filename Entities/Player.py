from os import path

import pygame

from Helpers.AnimatedSprite import AnimatedSprite


class Player(AnimatedSprite):
    INTERVAL = 120  # milliseconds between animation frame

    def __init__(self, picture, columns, rows, *groups, rect=None, speed=2, stages=None):
        if not rect:
            rect = pygame.Rect(0, 0, picture.get_width() // columns, picture.get_height() // rows)
        self.rect = rect
        self.speed = speed
        self.time = pygame.time.Clock()
        self.timer = 0
        self.x_dir = 0
        self.y_dir = 0

        super(Player, self).__init__(picture, columns, rows, rect.x, rect.y, *groups, stages=stages)

        self.stage = "Idle"

    def update(self, event=None):
        self.timer += self.time.tick()
        if self.timer >= self.INTERVAL:
            self.timer = 0
            if self.cur_frame + self.stages[self.stage][0] == self.stages["Die"][1] - 1:
                self.stopped = True
            elif self.cur_frame + self.stages[self.stage][0] == self.stages["Silence"][1] - 1 or self.cur_frame + \
                    self.stages[self.stage][0] == self.stages["Attack"][1] - 1:
                self.stage = "Idle"
            print(self.cur_frame)
            super().update()
        if event:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.stage = "Attack"
                self.cur_frame = 0
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    self.y_dir = -1
                if event.key == pygame.K_a:
                    self.x_dir = -1
                if event.key == pygame.K_s:
                    self.y_dir = 1
                if event.key == pygame.K_d:
                    self.x_dir = 1
                if event.key == pygame.K_x:
                    self.stage = "Die"
                if event.key == pygame.K_e and self.stage != "Die":
                    self.stage = "Silence"
                    self.cur_frame = 0
                    self.stopped = False
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    self.y_dir = self.y_dir = 0 if self.y_dir < 0 else self.y_dir
                if event.key == pygame.K_a:
                    self.x_dir = 0 if self.x_dir < 0 else self.x_dir
                if event.key == pygame.K_s:
                    self.y_dir = 0 if self.y_dir > 0 else self.y_dir
                if event.key == pygame.K_d:
                    self.x_dir = 0 if self.x_dir > 0 else self.x_dir
        else:
            self.move()

    def move(self):
        if self.stage == "Die" or self.stage == "Attack":
            return
        if self.x_dir == 0 and self.y_dir == 0:
            if self.stage == "Walk":
                self.stage = "Idle"
                self.cur_frame = 0
                self.stopped = False
            return
        self.x_flipped = self.x_flipped if self.x_dir == 0 else self.x_dir < 0
        self.stage = "Walk"
        self.stopped = False
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
    Player(load_image(["..", "data", "player.png"]), 8, 8, all_sprites, animated_sprites, stages={"Walk": [0, 8],
                                                                                                  "Idle": [8, 35],
                                                                                                  "Attack": [35, 41],
                                                                                                  "Silence": [41, 53],
                                                                                                  "Die": [54, 64]})
    running = True

    while running:
        screen.fill('blue')
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            all_sprites.update(event)
        all_sprites.draw(screen)
        animated_sprites.update()
        clock.tick(fps)
        pygame.display.flip()
    pygame.quit()
