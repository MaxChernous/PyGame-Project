import os
import sqlite3
from random import randint

import pygame
import pytmx.pytmx

from Game.Hero import Hero
from Game.Labyrinth import Labyrinth
from Game.Line import Line
from Game.Enemy import Enemy
from Game.Boss import Boss
from Helpers.Bombs import Bomb
from Helpers.helpers import *
from UI.Cursor import Cursor


class Game:

    def __init__(self, all_sprites, line_sprite, labyrinth, hero, enemies, screen, boss=None, bomb_sprites=None):
        self.all_sprites = all_sprites
        self.line_sprite = line_sprite
        self.bomb_sprites = bomb_sprites
        self.labyrinth = labyrinth
        self.hero = hero
        self.enemies = enemies
        self.screen = screen
        self.boss = boss
        self.hero_is_dead = False
        self.bombs = []

    def render(self, screen):
        self.labyrinth.render(screen)
        for enemy in self.enemies:
            enemy.update(screen)
        self.hero.update(screen)

    def update(self):
        next_x, next_y = self.hero.get_position()
        pushed = False
        if pygame.key.get_pressed()[pygame.K_a]:
            if self.labyrinth.is_free((next_x - 1, next_y)):
                self.hero.x_flipped = True
                next_x -= 1
                pushed = True
        if pygame.key.get_pressed()[pygame.K_d]:
            if self.labyrinth.is_free((next_x + 1, next_y)):
                self.hero.x_flipped = False
                next_x += 1
                pushed = True
        if pygame.key.get_pressed()[pygame.K_w]:
            if self.labyrinth.is_free((next_x, next_y - 1)):
                next_y -= 1
                pushed = True
        if pygame.key.get_pressed()[pygame.K_s]:
            if self.labyrinth.is_free((next_x, next_y + 1)):
                next_y += 1
                pushed = True
        if pushed and not self.hero.stage == "Attack":
            self.hero.stage = "Walk"
        elif not self.hero.stage == "Attack":
            self.hero.stage = "Idle"
        self.hero.set_position((next_x, next_y))

        if self.labyrinth.get_tile_id(self.hero.get_position()) == PISTOL_SPRITE:
            self.hero.weapon = "Pistol"

        for enemy in self.enemies:
            if ((enemy.get_position()[0] - self.hero.get_position()[0]) ** 2 + (
                    enemy.get_position()[1] - self.hero.get_position()[1]) ** 2) ** 0.5 <= enemy.radius_trigger:
                enemy.triggered = True

    def hero_strike(self, event_pos):
        self.hero.stage = "Attack"
        if self.hero.weapon == "Sword":
            for enemy in self.enemies:
                if abs(self.hero.get_position()[0] - enemy.get_position()[0]) <= 2 and \
                        abs(self.hero.get_position()[1] - enemy.get_position()[1]) <= 2:
                    enemy.life = False
                    break

        if self.hero.weapon == "Pistol":
            hit_line = Line(self.line_sprite, self.screen,
                            ((self.hero.get_position()[0] + 0.5) * TILE_SIZE,
                             (self.hero.get_position()[1] + 0.5) * TILE_SIZE), event_pos)

            for enemy in self.enemies:
                if pygame.sprite.collide_mask(hit_line, enemy):
                    enemy.life = False
                    break

            if self.boss:
                if pygame.sprite.collide_mask(hit_line, self.boss):
                    self.boss.damage()

    def boss_attack(self):
        for y in range(1, 18):
            for x in range(1, 20):
                if randint(1, 15) == 1:
                    if self.labyrinth.is_free((x, y), for_hero=False):
                        self.bombs.append(Bomb((x, y), self.bomb_sprites))

    def move_enemy(self):
        for enemy in self.enemies:
            if enemy.life and enemy.triggered:
                next_position = self.labyrinth.find_path_step(enemy.get_position(),
                                                              self.hero.get_position())
                enemy.set_position(next_position)

    def check_end(self):
        if self.boss:
            if self.boss.health_points > 0:
                return False
        return self.labyrinth.get_tile_id(self.hero.get_position()) == self.labyrinth.finish_tile

    def check_lose(self):
        if self.boss:
            for bomb in self.bombs:
                if bomb.updates_count == 9:
                    if abs(self.hero.get_position()[0] - bomb.x) <= 1 \
                            and abs(self.hero.get_position()[1] - bomb.y) <= 1:
                        self.hero_is_dead = True

        if self.hero_is_dead:
            return True

        if self.labyrinth.get_tile_id(self.hero.get_position()) == self.labyrinth.cactus_tile:
            return True

        for enemy in self.enemies:
            if self.hero.get_position() == enemy.get_position() and enemy.life:
                return True

        return False


def message(text, screen):
    font = pygame.font.Font(None, 50)
    text = font.render(text, True, "white")
    text_x = (WIDTH - text.get_width()) // 2
    text_y = (HEIGHT - text.get_height()) // 2 - 100
    text_w = text.get_width()
    text_h = text.get_height()
    pygame.draw.rect(screen, "black", (text_x - 10, text_y - 10, text_w + 20, text_h + 20))
    screen.blit(text, (text_x, text_y))


def show_stopwatch(stopwatch, screen):
    font = pygame.font.Font(None, 20)
    text = font.render(str(stopwatch), True, "white")
    text_w = text.get_width()
    text_h = text.get_height()
    pygame.draw.rect(screen, "black", (5, 5, text_w + 10, text_h + 10))
    screen.blit(text, (10, 10))


def write_result(stopwatch):
    con = sqlite3.connect("best_results.sqlite")
    cur = con.cursor()
    result = cur.execute(f'''SELECT time FROM records
                            WHERE time > {stopwatch}''').fetchall()
    if result:
        cur.execute(f'''UPDATE records
                    SET time = "{stopwatch}"
                    WHERE title = "the best result"
                    ''')
    con.commit()
    con.close()


def drw_line(line_sprite, screen):
    line_sprite.update(screen)
    line_sprite.draw(screen)


def main():
    pygame.init()
    screen = pygame.display.set_mode(SIZE)
    clock = pygame.time.Clock()
    stopwatch = 0

    all_sprites = pygame.sprite.Group()
    players = pygame.sprite.Group()
    line_sprite = pygame.sprite.Group()
    cursors = pygame.sprite.Group()
    bomb_sprites = pygame.sprite.Group()

    cursor = Cursor(pygame.transform.scale(
        load_image("cursor.png"), (50, 50)), cursors)

    hero = Hero(load_image("player.png"), 8, 8, all_sprites, players,
                rect=pygame.rect.Rect((1, 17), (TILE_SIZE, TILE_SIZE)),
                stages={"Walk": [0, 8],
                        "Idle": [8, 35],
                        "Attack": [35, 41],
                        "Silence": [41, 53],
                        "Die": [54, 64]}, weapon="Sword")

    enemy1 = Enemy(all_sprites, (4, 2), 100, 5)
    enemy2 = Enemy(all_sprites, (5, 17), 100, 5)
    enemy3 = Enemy(all_sprites, (8, 8), 100, 5)
    enemy4 = Enemy(all_sprites, (14, 4), 100, 3)

    labyrinth1 = Labyrinth("map1.tmx", [enemy1, enemy2, enemy3, enemy4])
    game = Game(all_sprites, line_sprite, labyrinth1,
                hero, [enemy1, enemy2, enemy3, enemy4], screen)
    level = 1

    score = pygame.time.Clock()
    number_score = 0
    timer = pygame.time.Clock()
    cooldown = 1000  # time before game closes

    running = True
    game_over = False
    while running:
        number_score += score.tick()
        game.labyrinth.render(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEMOTION:
                cursors.update(event.pos)

            if not game_over:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    game.hero_strike(event.pos)

                if event.type == ENEMY_EVENT_TYPE:
                    game.move_enemy()

                if event.type == BOSS_EVENT_TYPE:
                    if game.boss:
                        if game.boss.health_points > 0:
                            game.boss_attack()

                if event.type == STOPWATCH_EVENT_TYPE:
                    if not game_over:
                        stopwatch += 1

            all_sprites.update(screen)

        if game.check_end():
            if level == 1:
                labyrinth2 = Labyrinth("map2.tmx", [enemy1, enemy2, enemy3, enemy4])
                hero.set_position((1, 17))
                enemy1.set_position((6, 17))
                enemy2.set_position((3, 7))
                enemy3.set_position((19, 1))
                enemy4.set_position((19, 2))

                enemy2.radius_trigger = 6
                enemy3.radius_trigger = 8
                enemy4.radius_trigger = 8

                enemy1.delay = 50
                enemy2.delay = 50
                enemy3.delay = 10
                enemy4.delay = 10

                for enemy in game.enemies:
                    enemy.life = True
                    enemy.triggered = False

                game = Game(all_sprites, line_sprite, labyrinth2,
                            hero, [enemy1, enemy2, enemy3, enemy4], screen)
                level = 2

            elif level == 2:
                labyrinth3 = Labyrinth("map3.tmx", [])
                hero.set_position((2, 17))
                for enemy in game.enemies:
                    enemy.kill()
                    # enemy.delay = 25
                    # enemy.life = True
                    # enemy.triggered = False
                    # enemy.radius_trigger = 7

                enemy1.set_position((3, 18))
                enemy2.set_position((6, 12))
                enemy3.set_position((15, 14))
                enemy4.set_position((3, 6))

                boss = Boss(all_sprites, (8, 8))

                game = Game(all_sprites, line_sprite, labyrinth3,
                            hero, [], screen, boss=boss, bomb_sprites=bomb_sprites)
                level = 3

            else:
                if not game_over:
                    timer.tick()
                game_over = True
                mess = "You win! :)"
                cooldown -= timer.tick()
                if cooldown < 0:
                    return "win", (number_score + score.tick()) // 100

        if game.check_lose():
            if not game_over:
                timer.tick()
            game_over = True
            hero.stage = "Die"
            mess = "You lose! :("
            cooldown -= timer.tick()
            if cooldown < 0:
                return "Loose", (number_score + score.tick()) // 100

        if not game_over:
            game.update()
            screen.fill((0, 0, 0))
            game.render(screen)

        clock.tick(FPS)
        all_sprites.draw(screen)

        line_sprite.update(screen)
        line_sprite.draw(screen)

        bomb_sprites.update(screen)
        bomb_sprites.draw(screen)

        players.update(screen)
        players.draw(screen)
        show_stopwatch(number_score / 1000, screen)

        if pygame.mouse.get_focused():
            cursors.draw(screen)
        if game_over:
            message(mess, screen)
        pygame.display.flip()
    pygame.quit()


if __name__ == "__main__":
    main()
