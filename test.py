import os
import sys
import pygame
import requests

def change(coords_list, map_file, z):
    coords = ",".join(coords_list)
    map_request = f"http://static-maps.yandex.ru/1.x/?ll={coords}&l=map&z={z}"
    response = requests.get(map_request)

    if not response:
        print("Ошибка выполнения запроса:")
        print(map_request)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        return False

    with open(map_file, "wb") as file:
        file.write(response.content)
    return True

WINDOW_WIDTH, WINDOW_HEIGHT = 600, 450
z = 6
map_file = "map.png"
coords_list = input("Введите координаты через пробел: ").split()
change(coords_list, map_file, z)

pygame.init()
screen = pygame.display.set_mode((600, 450))
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if z <= 18:
                    z += 1
                    change(coords_list, map_file, z)
            if event.key == pygame.K_DOWN:
                if z >= 4:
                    z -= 1
                    change(coords_list, map_file, z)

    screen.blit(pygame.image.load(map_file), (0, 0))
    pygame.display.flip()

pygame.quit()
os.remove(map_file)
