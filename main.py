import pygame
from datetime import datetime

from Helpers.helpers import load_image
from States.BestResults import BestResults
from States.EndScreen import EndScreen
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
    screen = pygame.display.set_mode(size)
    cur = Cursor(pygame.transform.scale(
        load_image("cursor.png"), (50, 50)), cursor)
    pygame.mouse.set_visible(False)
    running = True
    main = Main()
    best_result_screen = BestResults(screen, main=main)
    requester = best_result_screen.requester

    win_end_image = pygame.transform.scale(load_image("win_end_image.png"), (height / 10 * 8, height))

    menu = MainMenu(screen, main=main)
    win_screen = EndScreen(screen, "Congratulations!", win_end_image, 10, main=main, won=True)
    loose_screen = EndScreen(screen, "You lost! Nice try", win_end_image, 20, main=main,
                             won=False)  # TODO : text and image for losing
    end_screen = loose_screen

    # Background music
    background_music_in_game = "data\\background_music.wav"
    menu_music = "data\\menu_music.mp3"

    pygame.mixer.music.load(menu_music)
    pygame.mixer.music.play()
    while running:
        screen.fill('black')
        if main.game_state == "main menu":
            menu.display(screen)
        if main.game_state == "best results":
            best_result_screen.display(screen)
        if main.game_state == "in game":
            pygame.mixer.music.load(background_music_in_game)
            pygame.mixer.music.play(-1)
            game_result = Gungeon.main()
            main.change_state("end game")
            if game_result[0] == "Loose":
                end_screen = loose_screen
            else:
                end_screen = win_screen
                requester.add_new_result(game_result[1], str(datetime.now().strftime("%D %H:%M:%S")))
            best_result_screen.item_changed()
            screen = pygame.display.set_mode(size)
            end_screen.set_score(game_result[1])
            pygame.mixer.music.stop()
            pygame.mixer.music.load(menu_music)
            pygame.mixer.music.play()
        if main.game_state == "end game":
            end_screen.display(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEMOTION:
                cursor.update(event.pos)
            all_sprites.update(event)
            if main.game_state == "main menu":
                menu.update(event)
            if main.game_state == "end game":
                end_screen.update(event)
            if main.game_state == "best results":
                best_result_screen.update(event)
        if main.game_state == "end game":
            end_screen.update()
        all_sprites.draw(screen)
        if pygame.mouse.get_focused():
            cursor.draw(screen)
        clock.tick(fps)
        pygame.display.flip()
    pygame.quit()
