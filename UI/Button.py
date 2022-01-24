import pygame

from pygame.sprite import AbstractGroup


class Button(pygame.sprite.Sprite):

    def __init__(self, color, *groups: AbstractGroup, image=None, text=pygame.Surface([0, 0]), rect=None):
        self.btn_color, self.btn_text = color, text
        super().__init__(*groups)
        if image:
            self.image = image
        else:
            self.image = pygame.Surface([text.get_width() + 20, text.get_height() + 20])
            self.image.blit(self.btn_text, (10, 10, text.get_height(), text.get_width()))
            pygame.draw.rect(self.image, (0, 255, 0), (0, 0, text.get_width() + 20, text.get_height() + 20), 2)

        if rect:
            self.rect = pygame.rect.Rect(rect)
        else:
            self.rect = self.image.get_rect()
        self.pushed = []
        self.clicked = []
        self.first = True

    def add_on_btn_down(self, method):
        self.pushed.append(method)

    def add_on_btn_up(self, method):
        # hsv = self.btn_color.hsva
        # self.color.hsva = (hsv[0], hsv[1], hsv[2] - 30, hsv[3])
        self.clicked.append(method)

    # def mouse_on_btn(self):
    #     hsv = self.btn_color.hsva
    #     # self.color.hsva = (hsv[0], hsv[1], hsv[2] - 15, hsv[3])

    def update(self, event=None):
        if event:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.first and self.check_click_position(event.pos):
                    self.first = False
                    for i in self.pushed:
                        i(event)

            if event.type == pygame.MOUSEBUTTONUP:
                for i in self.clicked:
                    i(event)
                self.first = True

    def draw(self, screen):
        screen.blit(self.btn_text, self.rect)

    def move_to(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def set_sprite(self, sprite):
        self.image = sprite

    def check_click_position(self, pos):
        x = self.rect.x
        y = self.rect.y
        return 0 <= (pos[0] - x) < self.rect.width and 0 <= (pos[1] - y) < self.rect.height
