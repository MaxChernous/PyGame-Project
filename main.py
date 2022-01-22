from os import path
from sys import exit

import pygame
from UI.Button import Button
from UI.Cursor import Cursor
from pygame.sprite import AbstractGroup


class Main_Menu_Image(pygame.sprite.Sprite):

    def __init__(self, *group):
        super().__init__(*group)
        self.image = pygame.transform.scale(load_image("main_menu_image.png"), (700, 600))
        self.rect = self.image.get_rect()
        self.rect.x = 720
        self.rect.y = 235


def down(event):
    print(1)


def load_image(name):
    fullname = path.join('data', name)
    if not path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        exit()
    image = pygame.image.load(fullname)
    return image


def create_main_menu(screen):
    game_name_text = pygame.font.Font(None, 75).render("Name of the Game", True, (255, 255, 100))
    game_name_text_x = width // 2 - game_name_text.get_width() // 2 - 250
    game_name_text_y = height // 2 - game_name_text.get_height() // 2 - 300
    game_name_text_w = game_name_text.get_width()
    game_name_text_h = game_name_text.get_height()
    game_name_image = pygame.surface.Surface((game_name_text_w + 20, game_name_text_h + 20))
    pygame.draw.rect(game_name_image, (255, 255, 0), (0, 0,
                                                      game_name_text_w + 20, game_name_text_h + 20), 2)
    game_name_image.blit(game_name_text, (10, 10))
    game_name_sprite = pygame.sprite.Sprite(all_sprites)
    game_name_sprite.image = game_name_image
    game_name_sprite.rect = (game_name_text_x, game_name_text_y, game_name_text_w, game_name_text_h)

    menu_text = pygame.font.Font(None, 60).render("Main menu", True, (100, 255, 100))
    menu_text_x, menu_text_y = width // 2 - menu_text.get_width() // 2 - 250, game_name_text_y + 150
    menu_text_sprite = pygame.sprite.Sprite(all_sprites)
    menu_text_sprite.image = menu_text
    menu_text_sprite.rect = menu_text.get_rect()
    menu_text_sprite.rect.x = menu_text_x
    menu_text_sprite.rect.y = menu_text_y

    # play button
    play_btn_text = pygame.font.Font(None, 45).render("Play", True, (100, 255, 100))
    play_btn_text_w, play_btn_text_h = play_btn_text.get_width(), play_btn_text.get_height()
    play_btn_x, play_btn_y = width // 2 - play_btn_text_w // 2 - 260, menu_text_y + 130
    play_btn = Button(pygame.Color((100, 255, 100)), play_btn_text,
                      rect=[play_btn_x, play_btn_y,
                            play_btn_text_w + 20, play_btn_text_h + 20])
    play_btn.add(all_sprites)

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
    leaderboard_btn.add_on_btn_down(down)
    leaderboard_btn.add(all_sprites)

    screen.blit(game_name_text, (game_name_text_x, game_name_text_y))
    screen.blit(menu_text, (menu_text_x, menu_text_y))
    # play_btn.update(screen)
    # leaderboard_btn.update(screen)


def draw_main_menu(screen):
    all_sprites.draw(screen)


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
    cur = Cursor(pygame.transform.scale(load_image("cursor.png"), (50, 50)), cursor)
    pygame.mouse.set_visible(False)
    running = True

    create_main_menu(screen)

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
