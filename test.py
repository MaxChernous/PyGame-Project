import os
import sys
import pygame
import requests

z = 6

pygame.init()
screen = pygame.display.set_mode((600, 450))
coords = ",".join(input("Введите координаты через пробел: ").split())
map_request = f"http://static-maps.yandex.ru/1.x/?ll={coords}&l=map&z={z}"
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if z <= 18:
                    z += 1
            if event.key == pygame.K_DOWN:
                if z >= 4:
                    z -= 1

    map_request = f"http://static-maps.yandex.ru/1.x/?ll={coords}&l=map&z={z}"
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
        screen.blit(pygame.image.load(map_file), (0, 0))

    pygame.display.flip()

pygame.quit()
os.remove(map_file)
