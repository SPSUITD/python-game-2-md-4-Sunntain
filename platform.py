import pygame

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        # Создание изображения и прямоугольника для платформы
        self.image = pygame.Surface((width, height))
        platform_texture = pygame.image.load("resources/platform.png")
        self.image.blit(platform_texture, (0, 0))
        self.rect = self.image.get_rect()
        # Позиционирование платформы
        self.rect.x = x
        self.rect.y = y