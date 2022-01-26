import pygame

from Helpers.helpers import load_image
from UI.Button import Button


class MainMenu:
    BTN_INTERVAL = 50

    def __init__(self, screen: pygame.surface.Surface):
        self.all_sprites = pygame.sprite.Group()
        width: int = screen.get_width()
        height = screen.get_height()

        game_name_text = pygame.font.Font(None, 75).render(
            "Name of the Game", True, (255, 255, 100))
        game_name_text_x = width // 2 - game_name_text.get_width() // 2 - 250
        game_name_text_y = height // 2 - game_name_text.get_height() // 2 - 300
        game_name_text_w = game_name_text.get_width()
        game_name_text_h = game_name_text.get_height()
        game_name_image = pygame.surface.Surface(
            (game_name_text_w + 20, game_name_text_h + 20))
        pygame.draw.rect(game_name_image, (255, 255, 0), (0, 0,
                                                          game_name_text_w + 20, game_name_text_h + 20), 2)
        game_name_image.blit(game_name_text, (10, 10))
        self.game_name_sprite = pygame.sprite.Sprite(self.all_sprites)
        self.game_name_sprite.image = game_name_image
        self.game_name_sprite.rect = pygame.rect.Rect(
            game_name_text_x, game_name_text_y, game_name_text_w, game_name_text_h
        )

        menu_text = pygame.font.Font(None, 60).render(
            "Main menu", True, (100, 255, 100))
        menu_text_x, menu_text_y = width // 2 - menu_text.get_width() // 2 - \
            250, game_name_text_y + 150
        self.menu_text_sprite = pygame.sprite.Sprite(self.all_sprites)
        self.menu_text_sprite.image = menu_text
        self.menu_text_sprite.rect = menu_text.get_rect()
        self.menu_text_sprite.rect.x = menu_text_x
        self.menu_text_sprite.rect.y = menu_text_y

        # play button
        play_btn_text = pygame.font.Font(None, 45).render(
            "Play", True, (100, 255, 100))
        play_btn_text_w, play_btn_text_h = play_btn_text.get_width(), play_btn_text.get_height()
        play_btn_x, play_btn_y = width // 2 - \
            play_btn_text_w // 2 - 260, menu_text_y + 130
        self.play_btn = Button(pygame.Color((100, 255, 100)), text=play_btn_text,
                               rect=pygame.rect.Rect(play_btn_x, play_btn_y,
                                                     play_btn_text_w + 20, play_btn_text_h + 20))
        self.play_btn.add(self.all_sprites)
        self.play_btn.add_on_btn_down(self.on_play_click)

        # leaderboard button
        leaderboard_btn_text = pygame.font.Font(None, 45).render(
            "Leaderboard", True, (100, 255, 100))
        leaderboard_btn_text_w, leaderboard_btn_text_h = leaderboard_btn_text.get_width(
        ), leaderboard_btn_text.get_height()
        leaderboard_btn_x = width // 2 - leaderboard_btn_text_w // 2 - 260
        leaderboard_btn_y = menu_text_y + 130 + self.BTN_INTERVAL + play_btn_text_h
        self.leaderboard_btn = Button(pygame.Color((100, 255, 100)), text=leaderboard_btn_text,
                                      rect=pygame.rect.Rect(leaderboard_btn_x, leaderboard_btn_y,
                                                            leaderboard_btn_text_w + 20, leaderboard_btn_text_h + 20))
        self.leaderboard_btn.add(self.all_sprites)
        self.leaderboard_btn.add_on_btn_down(self.on_leaderboard_click)

        # Menu Image
        self.menu_image = pygame.sprite.Sprite(self.all_sprites)
        self.menu_image.image = pygame.transform.scale(
            load_image("main_menu_image.png"), (700, 600))
        self.menu_image.rect = self.menu_image.image.get_rect()
        self.menu_image.rect.x = 720
        self.menu_image.rect.y = 235

    def display(self, screen: pygame.surface.Surface):
        self.all_sprites.draw(screen)

    def update(self, event: pygame.event.Event):
        self.all_sprites.update(event)

    def on_play_click(self, event: pygame.event.Event):
        print(event.pos, "Do you want to play?")

    def on_leaderboard_click(self, event: pygame.event.Event):
        print(event.pos, "Do you want to see the best score?")
