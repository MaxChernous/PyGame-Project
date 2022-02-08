import pygame

from Helpers.helpers import load_image
from States.MainMenu import MainMenu
from States import Gungeon

from UI.Cursor import Cursor


class Main:
    game_state = "main menu"

    def change_state(self, state):
        self.game_state = state


if __name__ == '__main__':
    pygame.init()
    size = width, height = 1350, 825
    fps = 300
    clock = pygame.time.Clock()
    all_sprites = pygame.sprite.Group()
    cursor = pygame.sprite.Group()
    game_state = "main menu"
    screen = pygame.display.set_mode(size)
    cur = Cursor(pygame.transform.scale(
        load_image("cursor.png"), (50, 50)), cursor)
    pygame.mouse.set_visible(False)
    running = True
    main = Main()

    menu = MainMenu(screen, main=main)

    while running:
        screen.fill('black')
        if main.game_state == "main menu":
            menu.display(screen)
        if main.game_state == "in game":
            Gungeon.main()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEMOTION:
                cursor.update(event.pos)
            all_sprites.update(event)
            if game_state == "main menu":
                menu.update(event)
        all_sprites.draw(screen)
        if pygame.mouse.get_focused():
            cursor.draw(screen)
        clock.tick(fps)
        pygame.display.flip()
    pygame.quit()
