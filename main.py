from os import path
from sys import exit

import pygame

from pygame.sprite import AbstractGroup


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


class Main_Menu_Image(pygame.sprite.Sprite):

    def __init__(self, *group):
        super().__init__(*group)
        self.image = pygame.transform.scale(load_image("main_menu_image.png"), (700, 600))
        self.rect = self.image.get_rect()
        self.rect.x = 720
        self.rect.y = 235

class Button:

    def btn_pushed(self):
        self.color.hsva = (self.btn_color.hsva[0], self.btn_color.hsva[1],
                           self.btn_color.hsva[2] + 30, self.btn_color.hsva[3])

    def btn_clicked(self):
        self.color.hsva = (self.btn_color.hsva[0], self.btn_color.hsva[1],
                           self.btn_color.hsva[2] + 30, self.btn_color.hsva[3])

    def __init__(self, color, text, *groups: AbstractGroup, image=None, rect=None):
        self.btn_color, self.btn_text = color, text
        super().__init__(*groups)
        if image:
            self.image = image
        else:
            self.image = pygame.Surface([100, 100])

        if rect:
            self.rect = rect
        else:
            self.rect = self.image.get_rect()
        self.pushed = []
        self.clicked = []

    def add_on_btn_down(self, method):
        self.pushed.append(method)

    def add_on_btn_up(self, method):
        hsv = self.btn_color.hsva
        self.color.hsva = (hsv[0], hsv[1], hsv[2] - 30, hsv[3])
        self.clicked.append(method)

    def mouse_on_btn(self):
        hsv = self.btn_color.hsva
        self.color.hsva = (hsv[0], hsv[1], hsv[2] - 15, hsv[3])

    def update(self, screen, event=None):
        screen.blit(self.btn_text, (self.rect[0], self.rect[1]))
        if event:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.btn_pushed()
                print(1)
                for i in self.pushed:
                    i(event)

            if event.type == pygame.MOUSEBUTTONUP:
                self.btn_clicked()
                print(1)
                for i in self.clicked:
                    i(event)

    def moveTo(self, x, y):
        self.btn_x = x
        self.btn_y = y

    def setSprite(self, sprite):
        self.image = sprite


def load_image(name):
    fullname = path.join('data', name)
    if not path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        exit()
    image = pygame.image.load(fullname)
    return image


def draw_main_menu(screen):
    game_name_text = pygame.font.Font(None, 75).render("Name of the Game", True, (255, 255, 100))
    game_name_text_x = width // 2 - game_name_text.get_width() // 2 - 250
    game_name_text_y = height // 2 - game_name_text.get_height() // 2 - 300
    game_name_text_w = game_name_text.get_width()
    game_name_text_h = game_name_text.get_height()
    pygame.draw.rect(screen, (255, 255, 0), (game_name_text_x - 10, game_name_text_y - 10,
                                             game_name_text_w + 20, game_name_text_h + 20), 2)

    menu_text = pygame.font.Font(None, 60).render("Main menu", True, (100, 255, 100))
    menu_text_x, menu_text_y = width // 2 - menu_text.get_width() // 2 - 250, game_name_text_y + 150

    # play button
    play_btn_text = pygame.font.Font(None, 45).render("Play", True, (100, 255, 100))
    play_btn_text_w, play_btn_text_h = play_btn_text.get_width(), play_btn_text.get_height()
    play_btn_x, play_btn_y = width // 2 - play_btn_text_w // 2 - 260, menu_text_y + 130
    play_btn = Button(pygame.Color((100, 255, 100)), play_btn_text,
                      rect=[play_btn_x, play_btn_y,
                            play_btn_text_w + 20, play_btn_text_h + 20])

    pygame.draw.rect(screen, (0, 255, 0), (play_btn_x - 10, play_btn_y - 10,
                                           play_btn_text_w + 20, play_btn_text_h + 20), 2)

    # leaderboard button
    leaderboard_btn_text = pygame.font.Font(None, 45).render("Leaderboard", True, (100, 255, 100))
    leaderboard_btn_text_w, leaderboard_btn_text_h = leaderboard_btn_text.get_width(), leaderboard_btn_text.get_height()
    leaderboard_btn_x = width // 2 - leaderboard_btn_text_w // 2 - 260
    leaderboard_btn_y = menu_text_y + 130 + btn_interval + play_btn_text_h
    leaderboard_btn = Button(pygame.Color((100, 255, 100)), leaderboard_btn_text,
                             rect=[leaderboard_btn_x, leaderboard_btn_y,
                                   leaderboard_btn_text_w + 20, leaderboard_btn_text_h + 20])
    pygame.draw.rect(screen, (0, 255, 0), (leaderboard_btn_x - 10, leaderboard_btn_y - 10,
                                           leaderboard_btn_text_w + 20, leaderboard_btn_text_h + 20), 2)

    screen.blit(game_name_text, (game_name_text_x, game_name_text_y))
    screen.blit(menu_text, (menu_text_x, menu_text_y))
    play_btn.update(screen)
    leaderboard_btn.update(screen)


if __name__ == '__main__':
    pygame.init()
    size = width, height = 1350, 825
    fps = 300
    btn_interval = 50
    clock = pygame.time.Clock()
    all_sprites = pygame.sprite.Group()
    cursor = pygame.sprite.Group()
    main_menu_image = Main_Menu_Image(all_sprites)
    game_state = "main menu"
    screen = pygame.display.set_mode(size)
    cur = Cursor(cursor)
    pygame.mouse.set_visible(False)
    running = True
    while running:
        screen.fill('black')
        if game_state == "main menu":
            draw_main_menu(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEMOTION:
                cursor.update(event.pos)
            all_sprites.update(event)
        all_sprites.draw(screen)
        if pygame.mouse.get_focused():
            cursor.draw(screen)
        clock.tick(fps)
        pygame.display.flip()
    pygame.quit()
