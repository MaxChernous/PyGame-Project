import sys

import pygame
import requests

WINDOW_W, WINDOW_H = 750, 490


def show_map():
    map_request = f"http://static-maps.yandex.ru/1.x/?ll={coords}&l={l}&z={z}"
    response = requests.get(map_request)
    if not response:
        print("Ошибка выполнения запроса:")
        print(map_request)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)
    else:
        map_file = "map.png"
        with open(map_file, "wb") as file:
            file.write(response.content)
        screen.blit(pygame.image.load(map_file), (20, 20))


class Button:

    def __init__(self, image, x_pos, y_pos, text_input, action, arg):
        self.image = image
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_input = text_input
        self.text = main_font.render(self.text_input, True, "white")
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))
        self.action = action
        self.arg = arg

    def update(self):
        screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def checkForInput(self, position):
        if position[0] in range(self.rect.left, self.rect.right) \
                and position[1] in range(self.rect.top, self.rect.bottom):
            self.action(self.arg)

    def changeColor(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top,
                                                                                          self.rect.bottom):
            self.text = main_font.render(self.text_input, True, "green")
        else:
            self.text = main_font.render(self.text_input, True, "white")


def change_vision(new_l):
    global l
    l = new_l


pygame.init()
screen = pygame.display.set_mode((WINDOW_W, WINDOW_H))
pygame.display.set_caption("Button!")
main_font = pygame.font.SysFont("cambria", 20)

z, l = 6, "map"
coords = ",".join(input("Введите координаты через пробел: ").split())

button_surface = pygame.image.load("button.png")
button_surface = pygame.transform.scale(button_surface, (100, 30))

scheme_button = Button(button_surface, 690, 30, "Схема", lambda x: change_vision(x), "map")
satellite_button = Button(button_surface, 690, 75, "Спутник", lambda x: change_vision(x), "sat")
hybrid_button = Button(button_surface, 690, 120, "Гибрид", lambda x: change_vision(x), "sat,skl")

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            scheme_button.checkForInput(pygame.mouse.get_pos())
            satellite_button.checkForInput(pygame.mouse.get_pos())
            hybrid_button.checkForInput(pygame.mouse.get_pos())

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if z <= 18:
                    z += 1
            if event.key == pygame.K_DOWN:
                if z >= 4:
                    z -= 1

    screen.fill("black")
    show_map()

    scheme_button.update()
    satellite_button.update()
    hybrid_button.update()

    scheme_button.changeColor(pygame.mouse.get_pos())
    satellite_button.changeColor(pygame.mouse.get_pos())
    hybrid_button.changeColor(pygame.mouse.get_pos())

    pygame.display.update()
os.remove("map.png")
