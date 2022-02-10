import pygame

from Helpers.Requester import Requester
from UI.Button import Button
from UI.Cell import Cell


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
        self.x, self.y = int(self.width / 4), int(self.height / 4)
        self.cell_size = self.cell_width, self.cell_height = int(self.width / 4), int((self.height / 8 * 5) / 11)
        self.requester = Requester("best_results.sqlite")
        self.color = (255, 255, 200)
        self.cells = []
        rect = pygame.rect.Rect(self.x, self.y, self.cell_width, self.cell_height)
        self.cells.append(Cell(pygame.Rect(rect), "Total Score", self.color, self.all_sprites))
        rect.x += self.cell_width
        self.cells.append(Cell(pygame.Rect(rect), "Was played", self.color, self.all_sprites))
        rect.x = self.x
        for i in self.requester.get_all_results()[:10]:
            rect.y += self.cell_height
            self.cells.append(Cell(pygame.Rect(rect), str(i[0]), self.color, self.all_sprites))
            rect.x += self.cell_width
            self.cells.append(Cell(pygame.Rect(rect), str(i[1]), self.color, self.all_sprites))
            rect.x = self.x
        if len(self.cells) < 3:
            rect.y += self.cell_height
            self.cells.append(Cell(pygame.Rect(rect), "Here will be your score", self.color, self.all_sprites))
            rect.x += self.cell_width
            self.cells.append(Cell(pygame.Rect(rect), "Here will be time", self.color, self.all_sprites))
            rect.x = self.x

    def display(self, screen):
        self.all_sprites.draw(screen)

    def update(self, event=None):
        self.all_sprites.update(event)

    def on_menu_button_click(self, event=None):
        print(event.pos)
        self.main.change_state("main menu")

    def item_changed(self):
        self.color = (255, 255, 200)
        self.cells = []
        rect = pygame.rect.Rect(self.x, self.y, self.cell_width, self.cell_height)
        self.cells.append(Cell(pygame.Rect(rect), "Total Score", self.color, self.all_sprites))
        rect.x += self.cell_width
        self.cells.append(Cell(pygame.Rect(rect), "Was played", self.color, self.all_sprites))
        rect.x = self.x
        for i in sorted(self.requester.get_all_results())[:10]:
            rect.y += self.cell_height
            self.cells.append(Cell(pygame.Rect(rect), str(i[0]), self.color, self.all_sprites))
            rect.x += self.cell_width
            self.cells.append(Cell(pygame.Rect(rect), str(i[1]), self.color, self.all_sprites))
            rect.x = self.x


if __name__ == '__main__':
    pygame.init()
    size = width, height = 1350, 825
    screen = pygame.display.set_mode(size)
    all_sprites = pygame.sprite.Group()
    table = BestResults(screen)
    while pygame.event.wait().type != pygame.QUIT:
        all_sprites.update()
        all_sprites.draw(screen)
        table.update()
        table.display(screen)
        pygame.display.flip()
