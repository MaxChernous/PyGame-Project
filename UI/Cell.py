import pygame


class Cell(pygame.sprite.Sprite):
    CELL_OFFSET = 20  # between

    def __init__(self, rect: pygame.rect.Rect, text, color, *groups: pygame.sprite.AbstractGroup):
        super().__init__(*groups)
        self.text_font = pygame.font.Font(None, 30).render(text, True, color)
        if self.text_font.get_width() > rect.width or \
                self.text_font.get_height() > rect.height:
            self.text_font = pygame.transform.scale(self.text_font, (rect.width - self.CELL_OFFSET,
                                                                     (rect.width - self.CELL_OFFSET) /
                                                                     self.text_font.get_width() *
                                                                     self.text_font.get_height()))

        self.rect = rect
        self.image = pygame.Surface(rect.size)
        self.image.blit(self.text_font, (
            (rect.width / 2) - (self.text_font.get_width() / 2),
            (rect.height / 2) - (self.text_font.get_height() / 2),
            self.text_font.get_height(), self.text_font.get_width()))
        pygame.draw.rect(self.image, color, (0, 0, rect.width, rect.height), 2)


if __name__ == '__main__':
    pygame.init()
    size = width, height = 400, 400
    screen = pygame.display.set_mode(size)
    all_sprites = pygame.sprite.Group()
    cell = Cell(pygame.rect.Rect(50, 50, 100, 10), "Something", (100, 255, 100), all_sprites)
    while pygame.event.wait().type != pygame.QUIT:
        all_sprites.update()
        all_sprites.draw(screen)
        pygame.display.flip()
