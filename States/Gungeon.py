import os

import pygame
import pytmx.pytmx

from Entities.Player import Player
from Helpers.helpers import load_image

SIZE = WIDTH, HEIGHT = 672, 608
FPS = 15
MAPS_DIR = "maps"
TILE_SIZE = 32
ENEMY_EVENT_TYPE = 30
PISTOL_SPRITE = 39
RIFLE_SPRITE = 40
GAME_RESULT = "WIN"


class Line(pygame.sprite.Sprite):
    def __init__(self, group, screen, from_pos, to_pos):
        super().__init__(group)
        self.image = pygame.Surface(SIZE)
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0
        self.screen = screen

        self.from_pos = from_pos
        self.to_pos = to_pos
        self.dx = to_pos[0] - self.from_pos[0]
        self.dy = to_pos[1] - self.from_pos[1]
        pygame.draw.line(self.image, (0, 200, 0), self.from_pos, (to_pos[0] + self.dx * 1000,
                                                                  self.to_pos[1] + self.dy * 1000), 20)
        self.mask = pygame.mask.from_surface(self.image)

        self.updates_count = 0

    def update(self, screen):
        self.updates_count += 1
        if self.updates_count > 3:
            self.kill()


class Labyrinth:

    def __init__(self, filename, free_tiles, finish_tile, cactus_tile, enemies):
        fullname = os.path.join(MAPS_DIR, filename)
        self.map = pytmx.load_pygame(fullname)
        self.height = self.map.height
        self.width = self.map.width
        self.tile_size = self.map.tilewidth
        self.free_tiles = free_tiles
        self.finish_tile = finish_tile
        self.cactus_tile = cactus_tile
        self.enemies = enemies

    def render(self, screen):
        for y in range(self.height):
            for x in range(self.width):
                image = self.map.get_tile_image(x, y, 0)
                screen.blit(image, (x * self.tile_size, y * self.tile_size))

    def get_tile_id(self, position):
        return self.map.tiledgidmap[self.map.get_tile_gid(*position, 0)]

    def is_free(self, position, for_hero=True):
        if for_hero:
            return self.get_tile_id(position) in self.free_tiles
        else:
            return self.get_tile_id(position) in self.free_tiles and \
                   self.get_tile_id(position) != self.cactus_tile

    def find_path_step(self, start, target):
        INF = 10000
        x, y = start
        distance = [[INF] * self.width for _ in range(self.height)]
        distance[y][x] = 0
        prev = [[None] * self.width for _ in range(self.height)]
        queue = [(x, y)]
        while queue:
            x, y = queue.pop(0)
            for dx, dy in (1, 0), (0, 1), (-1, 0), (0, -1):
                next_x, next_y = x + dx, y + dy
                if 0 <= next_x < self.width and 0 < next_y < self.height and \
                        self.is_free((next_x, next_y), False) and distance[next_y][next_x] == INF:
                    distance[next_y][next_x] = distance[y][x] + 1
                    prev[next_y][next_x] = (x, y)
                    queue.append((next_x, next_y))
        x, y = target
        if distance[y][x] == INF or start == target:
            return start
        while prev[y][x] != start:
            x, y = prev[y][x]

        free = True
        for enemy in self.enemies:
            if enemy.get_position() == (x, y) and enemy.life:
                free = False
        if free:
            return x, y
        else:
            return start


class Hero(Player):
    sword_image = load_image("hero_sword_image.png")
    pistol_image = load_image("hero_pistol_image.png")
    rifle_image = load_image("hero_rifle_image.png")

    INTERVAL = 120  # milliseconds between animation frame
    OFFSET_X = TILE_SIZE / 1.5
    OFFSET_Y = TILE_SIZE / 1.5 + 5

    def __init__(self, picture, columns, rows, *groups, rect=None, speed=2, weapon, stages=None):
        if not rect:
            rect = pygame.Rect(0, 0, picture.get_width() // columns, picture.get_height() // rows)
        self.rect = rect
        self.speed = speed
        self.time = pygame.time.Clock()
        self.timer = 0
        self.x_dir = 0
        self.y_dir = 0
        self.weapon = weapon
        self.x = rect.x
        self.y = rect.y

        print(rect.x, rect.y)

        super(Hero, self).__init__(picture, columns, rows, *groups, rect=rect, stages=stages)

        self.stage = "Idle"

    def get_position(self):
        return self.x, self.y

    def set_position(self, position):
        self.x, self.y = position

    def update(self, screen):
        super().update()
        # if self.weapon == "Sword":
        #     self.image = Hero.sword_image
        # elif self.weapon == "Pistol":
        #     self.image = Hero.pistol_image
        # else:
        #     self.image = Hero.rifle_image

        self.image = pygame.transform.scale(self.image, (TILE_SIZE * 2.5, TILE_SIZE * 2.5))
        self.rect.x = self.x * TILE_SIZE - self.OFFSET_X
        self.rect.y = self.y * TILE_SIZE - self.OFFSET_Y
        self.mask = pygame.mask.from_surface(self.image)


class Enemy(pygame.sprite.Sprite):
    life_image = load_image("enemy_life_image.png")
    dead_image = load_image("enemy_dead_image.png")

    def __init__(self, group, position, delay, radius_trigger):
        super().__init__(group)
        self.image = Enemy.life_image
        self.image = pygame.transform.scale(self.image, (TILE_SIZE, TILE_SIZE))
        self.rect = self.image.get_rect()
        self.x, self.y = position
        self.rect.x = self.x * TILE_SIZE
        self.rect.y = self.y * TILE_SIZE
        self.delay = delay
        pygame.time.set_timer(ENEMY_EVENT_TYPE, self.delay)
        self.life = True
        self.triggered = False
        self.radius_trigger = radius_trigger
        self.mask = pygame.mask.from_surface(self.image)

    def get_position(self):
        return self.x, self.y

    def set_position(self, position):
        self.x, self.y = position

    def update(self, screen):
        if self.life:
            self.image = Enemy.life_image
        else:
            self.image = Enemy.dead_image

        self.image = pygame.transform.scale(self.image, (TILE_SIZE, TILE_SIZE))
        self.rect.x = self.x * TILE_SIZE
        self.rect.y = self.y * TILE_SIZE
        self.mask = pygame.mask.from_surface(self.image)


class Boss(pygame.sprite.Sprite):
    life_image = load_image("boss_life_image.png")
    dead_image = load_image("boss_dead_image.png")

    def __init__(self, group, position, delay, radius_trigger):
        super().__init__(group)
        self.image = Boss.life_image
        self.image = pygame.transform.scale(self.image, (TILE_SIZE, TILE_SIZE))
        self.rect = self.image.get_rect()
        self.x, self.y = position
        self.rect.x = self.x * TILE_SIZE
        self.rect.y = self.y * TILE_SIZE
        self.delay = delay
        pygame.time.set_timer(ENEMY_EVENT_TYPE, self.delay)
        self.life = True
        self.triggered = False
        self.radius_trigger = radius_trigger
        self.mask = pygame.mask.from_surface(self.image)


class Game:

    def __init__(self, all_sprites, line_sprite, labyrinth, hero, enemies, screen):
        self.all_sprites = all_sprites
        self.line_sprite = line_sprite
        self.labyrinth = labyrinth
        self.hero = hero
        self.enemies = enemies
        self.screen = screen

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
                self.hero.stage = "Walk" if self.hero.stage == "Idle" else self.hero.stage
                pushed = True
        if pygame.key.get_pressed()[pygame.K_d]:
            if self.labyrinth.is_free((next_x + 1, next_y)):
                self.hero.x_flipped = False
                next_x += 1
                self.hero.stage = "Walk" if self.hero.stage == "Idle" else self.hero.stage
                pushed = True
        if pygame.key.get_pressed()[pygame.K_w]:
            if self.labyrinth.is_free((next_x, next_y - 1)):
                next_y -= 1
                self.hero.stage = "Walk" if self.hero.stage == "Idle" else self.hero.stage
                pushed = True
        if pygame.key.get_pressed()[pygame.K_s]:
            if self.labyrinth.is_free((next_x, next_y + 1)):
                next_y += 1
                self.hero.stage = "Walk" if self.hero.stage == "Idle" else self.hero.stage
                pushed = True
        if not pushed and self.hero.stage == "Walk":
            self.hero.stage = "Idle"
        self.hero.set_position((next_x, next_y))

        if self.labyrinth.get_tile_id(self.hero.get_position()) == PISTOL_SPRITE:
            self.hero.weapon = "Pistol"
        elif self.labyrinth.get_tile_id(self.hero.get_position()) == RIFLE_SPRITE:
            self.hero.weapon = "Rifle"

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
            hit_line = Line(self.line_sprite, self.screen, ((self.hero.get_position()[0] + 0.5) * TILE_SIZE,
                                                            (self.hero.get_position()[1] + 0.5) * TILE_SIZE), event_pos)

            for enemy in self.enemies:
                if pygame.sprite.collide_mask(hit_line, enemy):
                    enemy.life = False
                    break

    def move_enemy(self):
        for enemy in self.enemies:
            if enemy.life and enemy.triggered:
                next_position = self.labyrinth.find_path_step(enemy.get_position(),
                                                              self.hero.get_position())
                enemy.set_position(next_position)

    def check_end(self):
        return self.labyrinth.get_tile_id(self.hero.get_position()) == self.labyrinth.finish_tile

    def check_lose(self):
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
    text_y = (HEIGHT - text.get_height()) // 2
    text_w = text.get_width()
    text_h = text.get_height()
    pygame.draw.rect(screen, "black", (text_x - 10, text_y - 10, text_w + 20, text_h + 20))
    screen.blit(text, (text_x, text_y))


def drw_line(line_sprite, screen):
    line_sprite.update(screen)
    line_sprite.draw(screen)


def main():
    pygame.init()
    screen = pygame.display.set_mode(SIZE)
    clock = pygame.time.Clock()

    all_sprites = pygame.sprite.Group()
    players = pygame.sprite.Group()
    line_sprite = pygame.sprite.Group()

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
    labyrinth1 = Labyrinth("map1.tmx", [30, 46, 31], 46, 31, [enemy1, enemy2, enemy3, enemy4])
    game = Game(all_sprites, line_sprite, labyrinth1, hero, [enemy1, enemy2, enemy3, enemy4], screen)
    level = 1
    cooldown = 2000  # Time before the end screen, ms
    timer = pygame.time.Clock()  # timer to count time before showing theend screen

    running = True
    game_over = False
    while running:
        game.labyrinth.render(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if not game_over:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    game.hero_strike(event.pos)

                if event.type == ENEMY_EVENT_TYPE:
                    game.move_enemy()
            all_sprites.update(screen)

        if game.check_end():
            if level == 1:
                labyrinth2 = Labyrinth("map2.tmx", [30, 46, 31, 39], 46, 31, [enemy1, enemy2, enemy3, enemy4])
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

                enemy1.life = True
                enemy2.life = True
                enemy3.life = True
                enemy4.life = True

                enemy1.triggered = False
                enemy2.triggered = False
                enemy3.triggered = False
                enemy4.triggered = False

                game = Game(all_sprites, line_sprite, labyrinth2, hero, [enemy1, enemy2, enemy3, enemy4], screen)
                level = 2

            elif level == 2:
                labyrinth3 = Labyrinth("map3.tmx", [30, 46, 31, 40], 46, 40, [enemy1, enemy2, enemy3, enemy4])
                hero.set_position((1, 17))
                enemy.set_position((19, 2))
                enemy.delay = 50
                enemy.life = True
                game = Game(labyrinth3, hero, enemy)
                level = 3

            else:
                game_over = True
                message("You win! :)", screen)

        if game.check_lose():
            if not game_over:
                timer.tick()
            game_over = True
            hero.stage = "Die"
            for enemy in game.enemies:
                enemy = None
            cooldown -= timer.tick()
            print(cooldown)
            message("You lose :(", screen)
            if cooldown < 0:
                return "Loose", 1000

        if not game_over:
            game.update()
            screen.fill((0, 0, 0))
            game.render(screen)

        clock.tick(FPS)
        all_sprites.draw(screen)

        line_sprite.update(screen)
        line_sprite.draw(screen)
        players.update(screen)
        players.draw(screen)

        pygame.display.flip()
    pygame.quit()


if __name__ == "__main__":
    main()
