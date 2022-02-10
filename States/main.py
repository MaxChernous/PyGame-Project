import pygame

from Helpers.helpers import load_image
from States.EndScreen import EndScreen
from States.MainMenu import MainMenu
from States import Gungeon_test

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
    cursors = pygame.sprite.Group()
    screen = pygame.display.set_mode(size)
    cursor = Cursor(pygame.transform.scale(
        load_image("cursor.png"), (50, 50)), cursors)
    pygame.mouse.set_visible(False)
    running = True
    main = Main()
    main.game_state = "main menu"

    win_end_image = pygame.transform.scale(load_image("win_end_image.png"), (height / 10 * 8, height))

    menu = MainMenu(screen, main=main)
    end_screen = EndScreen(screen, "Congrats", win_end_image, 10, main=main, won=True)

    while running:
        screen.fill('black')
        if main.game_state == "main menu":
            menu.display(screen)
        if main.game_state == "in game":
            Gungeon_test.main()
        if main.game_state == "end game":
            end_screen.display(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEMOTION:
                cursors.update(event.pos)
            all_sprites.update(event)
            if main.game_state == "main menu":
                menu.update(event)
            if main.game_state == "end game":
                end_screen.update(event)
        if main.game_state == "end game":
            end_screen.update()
        all_sprites.draw(screen)
        if pygame.mouse.get_focused():
            cursors.draw(screen)
        clock.tick(fps)
        pygame.display.flip()
    pygame.quit()
