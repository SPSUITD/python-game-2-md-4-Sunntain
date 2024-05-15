import pygame

class Door(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        # Создание изображения и прямоугольника для двери
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        door_texture = pygame.image.load("resources/door.png").convert_alpha()  # Загрузка текстуры для двери
        self.image.blit(door_texture, (0, 0))  # Наложение текстуры на изображение двери
        self.rect = self.image.get_rect()
        # Позиционирование двери
        self.rect.x = x
        self.rect.y = y
        # Флаг, указывающий, что дверь открыта
        self.opened = False

    def check_collision(self, player):
        # Проверка столкновения игрока с дверью
        if self.rect.colliderect(player.rect) and player.has_key:
            self.opened = True
            return True
        return False