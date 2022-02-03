import pygame
import pytmx.pytmx

SIZE = WIDTH, HEIGHT = 672, 608
FPS = 10
MAPS_DIR = "maps"
TILE_SIZE = 32
ENEMY_EVENT_TYPE = 30


class Labyrinth:

    def __init__(self, filename, free_tiles, finish_tile, cactus_tile, enemies):
        self.map = pytmx.load_pygame(f"{MAPS_DIR}/{filename}")
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

    def get_title_id(self, position):
        return self.map.tiledgidmap[self.map.get_tile_gid(*position, 0)]

    def is_free(self, position, for_hero=True):
        if for_hero:
            return self.get_title_id(position) in self.free_tiles
        else:
            return self.get_title_id(position) in self.free_tiles and \
                   self.get_title_id(position) != self.cactus_tile

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


class Hero:

    def __init__(self, position, weapon):
        self.x, self.y = position
        self.weapon = weapon

    def get_position(self):
        return self.x, self.y

    def set_position(self, position):
        self.x, self.y = position

    def render(self, screen):
        center = self.x * TILE_SIZE + TILE_SIZE // 2, \
                 self.y * TILE_SIZE + TILE_SIZE // 2
        pygame.draw.circle(screen, (0, 100, 200), center, TILE_SIZE // 2)


class Enemy:

    def __init__(self, position, delay, radius_trigger):
        self.x, self.y = position
        self.delay = delay
        pygame.time.set_timer(ENEMY_EVENT_TYPE, self.delay)
        self.life = True
        self.triggered = False
        self.radius_trigger = radius_trigger

    def get_position(self):
        return self.x, self.y

    def set_position(self, position):
        self.x, self.y = position

    def render(self, screen):
        center = self.x * TILE_SIZE + TILE_SIZE // 2, \
                 self.y * TILE_SIZE + TILE_SIZE // 2
        if self.life:
            pygame.draw.circle(screen, "red", center, TILE_SIZE // 2)
        else:
            pygame.draw.circle(screen, (100, 0, 0), center, TILE_SIZE // 5)


class Game:

    def __init__(self, labyrinth, hero, enemies):
        self.labyrinth = labyrinth
        self.hero = hero
        self.enemies = enemies

    def render(self, screen):
        self.labyrinth.render(screen)
        self.hero.render(screen)
        for enemy in self.enemies:
            enemy.render(screen)

    def update(self):
        next_x, next_y = self.hero.get_position()
        if pygame.key.get_pressed()[pygame.K_a]:
            if self.labyrinth.is_free((next_x - 1, next_y)):
                next_x -= 1
        if pygame.key.get_pressed()[pygame.K_d]:
            if self.labyrinth.is_free((next_x + 1, next_y)):
                next_x += 1
        if pygame.key.get_pressed()[pygame.K_w]:
            if self.labyrinth.is_free((next_x, next_y - 1)):
                next_y -= 1
        if pygame.key.get_pressed()[pygame.K_s]:
            if self.labyrinth.is_free((next_x, next_y + 1)):
                next_y += 1
        self.hero.set_position((next_x, next_y))

        for enemy in self.enemies:
            if ((enemy.get_position()[0] - self.hero.get_position()[0]) ** 2 + (
                    enemy.get_position()[1] - self.hero.get_position()[1]) ** 2) ** 0.5 <= enemy.radius_trigger:
                enemy.triggered = True

    def hero_strike(self):
        if self.hero.weapon == "Sword":
            for enemy in self.enemies:
                if abs(self.hero.get_position()[0] - enemy.get_position()[0]) <= 2 and \
                        abs(self.hero.get_position()[1] - enemy.get_position()[1]) <= 2:
                    enemy.life = False

    def move_enemy(self):
        for enemy in self.enemies:
            if enemy.life and enemy.triggered:
                next_position = self.labyrinth.find_path_step(enemy.get_position(),
                                                              self.hero.get_position())
                enemy.set_position(next_position)

    def check_end(self):
        return self.labyrinth.get_title_id(self.hero.get_position()) == self.labyrinth.finish_tile

    def check_lose(self):
        if self.hero.get_position() == 31:
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


def main():
    pygame.init()
    screen = pygame.display.set_mode(SIZE)
    clock = pygame.time.Clock()
    hero = Hero((1, 17), "Sword")
    enemy1 = Enemy((11, 5), 100, 5)
    enemy2 = Enemy((5, 17), 100, 5)
    enemy3 = Enemy((8, 8), 100, 5)
    enemy4 = Enemy((17, 7), 100, 5)
    labyrinth1 = Labyrinth("map1.tmx", [30, 46, 31], 46, 31, [enemy1, enemy2, enemy3, enemy4])
    game = Game(labyrinth1, hero, [enemy1, enemy2, enemy3, enemy4])
    level = 1
    running = True
    game_over = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                game.hero_strike()

            if event.type == ENEMY_EVENT_TYPE:
                game.move_enemy()

        if game.check_end():
            if level == 1:
                labyrinth2 = Labyrinth("map2.tmx", [30, 46, 31, 39], 46, 31, [enemy1, enemy2, enemy3, enemy4])
                hero.set_position((1, 17))
                enemy1.set_position((6, 17))
                enemy2.set_position((3, 8))
                enemy3.set_position((19, 1))
                enemy4.set_position((19, 2))

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

                game = Game(labyrinth2, hero, [enemy1, enemy2, enemy3, enemy4])
                level = 2

            elif level == 2:
                labyrinth3 = Labyrinth("map3.tmx", [30, 46, 31, 40], 46, 31)
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
            game_over = True
            message("You lose :(", screen)

        if not game_over:
            game.update()
            screen.fill((0, 0, 0))
            game.render(screen)

        clock.tick(FPS)
        pygame.display.flip()
    pygame.quit()


if __name__ == "__main__":
    main()
