import pygame

from Helpers.AnimatedSprite import AnimatedSprite
from Helpers.helpers import load_image
from UI.Button import Button


class EndScreen:
    EXPLOSION_OFFSET = 150

    def __init__(self, screen: pygame.surface.Surface, text, image: pygame.surface.Surface, score=0, main=None,
                 won=True):
        self.size = self.width, self.height = screen.get_size()
        self.all_sprites = pygame.sprite.Group()
        self.main = main

        # Image to make the screen more interesting
        self.decor_image = pygame.sprite.Sprite(self.all_sprites)
        self.decor_image.image = image
        self.decor_image.rect = image.get_rect()
        self.decor_image.rect.x = self.width - (image.get_width())
        self.decor_image.rect.y = self.height - (image.get_height())

        # Text field with results of game
        result_text = pygame.font.Font(None, 60).render(text, True, (255, 255, 100))
        self.result_text_sprite = pygame.sprite.Sprite(self.all_sprites)
        self.result_text_sprite.image = result_text
        self.result_text_sprite.rect = result_text.get_rect()
        self.result_text_sprite.rect.x = (self.width - self.decor_image.rect.x) / 2 - (result_text.get_width() / 2)
        self.result_text_sprite.rect.y = self.height / 4

        # Text field to show the score
        score_text = pygame.font.Font(None, 40).render("Your score: {}".format(score), True, (255, 255, 100))
        self.score_text_sprite = pygame.sprite.Sprite(self.all_sprites)
        self.score_text_sprite.image = score_text
        self.score_text_sprite.rect = score_text.get_rect()
        self.score_text_sprite.rect.x = (self.width - self.decor_image.rect.x) / 2 - (score_text.get_width() / 2)
        self.score_text_sprite.rect.y = self.height / 2
        self.set_score(score)

        # Button to main menu
        menu_button_text = pygame.font.Font(None, 45).render(
            "Main Menu", True, (100, 255, 100))
        menu_button_width, menu_button_height = menu_button_text.get_width(
        ), menu_button_text.get_height()
        menu_button_x = (self.width - self.decor_image.rect.x) / 2 - (menu_button_text.get_width() / 2)
        menu_button_y = self.height / 4 * 3
        self.menu_button = Button(pygame.Color((100, 255, 100)), text=menu_button_text,
                                  rect=pygame.rect.Rect(menu_button_x, menu_button_y,
                                                        menu_button_width + 20, menu_button_height + 20))
        self.menu_button.add(self.all_sprites)
        self.menu_button.add_on_btn_down(self.on_menu_button_click)

        # Some additional decor for winning
        if won:
            self.fireworks = []
            for i in range(3):
                self.fireworks.append(AnimatedSprite(load_image("confetti_explosion.png"), 5, 5,
                                                     (self.width - self.decor_image.rect.x) / 3 * i,
                                                     self.result_text_sprite.rect.y - self.EXPLOSION_OFFSET,
                                                     self.all_sprites, frame_per_second=15))

    def display(self, screen):
        self.all_sprites.draw(screen)

    def update(self, event=None):
        self.all_sprites.update(event)

    def set_score(self, score):
        score_text = pygame.font.Font(None, 40).render("Your score: {}".format(score), True, (255, 255, 100))
        self.score_text_sprite.image = score_text

    def on_menu_button_click(self, event=None):
        print("1")
        self.main.change_state("main menu")
