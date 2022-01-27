from os import path

import pygame


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y, *groups, stages=None):
        super().__init__(*groups)
        self.frames = []
        self.stopped = False
        if stages:
            self.stages = stages
        else:
            self.stages = {"Idle": [0, columns * rows]}
        self.stage = "Idle"
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)
        self.x_flipped = False
        self.y_flipped = False

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self, *args):
        if self.stopped:
            return
        self.cur_frame = (self.cur_frame + 1) % (self.stages[self.stage][1] - self.stages[self.stage][0])
        self.image = pygame.transform.flip(self.frames[self.cur_frame + self.stages[self.stage][0]], self.x_flipped,
                                           self.y_flipped)

    def flip_x(self):
        self.x_flipped = False

    def flip_y(self):
        self.y_flipped = False


def load_image(name):
    fullname = path.join('../data', name)
    if not path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        exit()
    image = pygame.image.load(fullname)
    return image


if __name__ == '__main__':
    size = width, height = 1350, 825
    fps = 30
    clock = pygame.time.Clock()
    all_sprites = pygame.sprite.Group()
    dinosaur = AnimatedSprite(load_image("dinosaur (test).bmp"), 8, 2, 10, 10, all_sprites)
    screen = pygame.display.set_mode(size)
    running = True
    last = 0

    while running:
        screen.fill('black')
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        all_sprites.draw(screen)
        pygame.display.flip()
    pygame.quit()
