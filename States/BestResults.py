import pygame

from Helpers.DataBase import Requester
from UI.Button import Button


class BestResults:
    BUTTON_POS = (10, 10)  # to position main menu button in left top corner

    def __init__(self, screen: pygame.surface.Surface, main=None):
        self.size = self.width, self.height = screen.get_size()
        self.all_sprites = pygame.sprite.Group()
        self.main = main

        # Button to main menu
        menu_button_text = pygame.font.Font(None, 30).render(
            "Main Menu", True, (100, 255, 100))
        menu_button_width, menu_button_height = menu_button_text.get_width(
        ), menu_button_text.get_height()
        menu_button_x, menu_button_y = self.BUTTON_POS
        self.menu_button = Button(pygame.Color((100, 255, 100)), text=menu_button_text,
                                  rect=pygame.rect.Rect(menu_button_x, menu_button_y,
                                                        menu_button_width + 20, menu_button_height + 20))
        self.menu_button.add(self.all_sprites)
        self.menu_button.add_on_btn_down(self.on_menu_button_click)

        # making table
        self.x, self.y = self.width / 4, self.height / 4
        self.cell_size = self.cell_width, self.cell_height = self.width / 4, (self.height / 8 * 5) / 11
        self.requester = Requester("best_results.sqlite")
        for i in range(self.requester.get_all_results()[:10]):
            pass

    def display(self, screen):
        self.all_sprites.draw(screen)

    def update(self, event=None):
        self.all_sprites.update(event)

    def on_menu_button_click(self, event=None):
        print("1")
        self.main.change_state("main menu")


if __name__ == '__main__':
    pass
