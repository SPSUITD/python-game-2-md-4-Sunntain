
import pygame

class Spike(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.spritesheet = pygame.image.load("resources/spike_spritesheet.png").convert_alpha()
        self.frame_width = width
        self.frame_height = height

        # Разбиение спрайтшита на отдельные кадры
        self.frames = []
        self.load_frames()

        # Установка начального кадра
        self.current_frame = 0
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        # Время, прошедшее с последнего обновления кадра
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 100  # Интервал между кадрами в миллисекундах

    def load_frames(self):
        sheet_width, sheet_height = self.spritesheet.get_size()
        for i in range(sheet_width // self.frame_width):
            frame = self.spritesheet.subsurface(pygame.Rect(
                i * self.frame_width, 0, self.frame_width, self.frame_height))
            self.frames.append(frame)

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.image = self.frames[self.current_frame]