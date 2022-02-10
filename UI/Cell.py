import pygame


class Cell(pygame.sprite.Sprite):
    CELL_OFFSET = 20  # between

    def __init__(self, rect: pygame.rect.Rect, text, *groups: pygame.sprite.AbstractGroup):
        super().__init__(*groups)
        self.text_font = pygame.font.Font(None, 30).render(text, True, (100, 255, 100))
        self.image = pygame.Surface(rect.size)
        self.image.blit(self.text_font, (
        rect.width / 2 - self.text_font.get_width() / 2, rect.height / 2 - self.text_font.get_height() / 2,
        text.get_height(), text.get_width()))
        pygame.draw.rect(self.image, (0, 255, 0), (0, 0,
                                                   text.get_width() + 20, text.get_height() + 20), 2)
