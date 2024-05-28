import pygame
from config import *

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Загрузка спрайтов и статических текстур
        self.spritesheet_right = pygame.image.load("resources/player_walk_right.png").convert_alpha()
        self.spritesheet_left = pygame.image.load("resources/player_walk_left.png").convert_alpha()
        self.image_stand_right = pygame.image.load("resources/player_stand_right.png").convert_alpha()
        self.image_stand_left = pygame.image.load("resources/player_stand_left.png").convert_alpha()

        # Установка начального изображения
        self.image = self.image_stand_right
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

        # Параметры для анимации
        self.frame_index = 0
        self.frame_rate = 100  # Интервал между кадрами в миллисекундах
        self.last_update = pygame.time.get_ticks()

        # Состояние игрока
        self.y_velocity = 0
        self.on_ground = False
        self.has_key = False
        self.direction = "right"  # Начальное направление

        # Таймер для столкновения с шипами
        self.spike_collision_time = 0
        self.control_disabled = False

    def update(self, platforms, spikes):
        current_time = pygame.time.get_ticks()

        # Обработка гравитации
        self.y_velocity += GRAVITY
        if self.y_velocity > MAX_FALL_SPEED:
            self.y_velocity = MAX_FALL_SPEED
        self.rect.y += self.y_velocity

        # Проверка вертикальных столкновений
        self.check_collision_y(platforms)

        # Проверка столкновений с шипами
        self.check_collision_spikes(spikes)

        # Проверка горизонтальных границ экрана
        if self.rect.left > SCREEN_WIDTH:
            self.rect.right = 0
        elif self.rect.right < 0:
            self.rect.left = SCREEN_WIDTH

        if self.control_disabled and current_time - self.spike_collision_time < 1000:
            return  # Блокировка управления на 1 секунду

        if self.control_disabled and current_time - self.spike_collision_time >= 1000:
            self.control_disabled = False

        # Обработка прыжка и движения влево/вправо
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.on_ground:
            self.y_velocity = JUMP_POWER
            self.on_ground = False

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= MOVE_SPEED
            self.handle_collision_x(platforms)
            self.direction = "left"
            self.animate(self.spritesheet_left)
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += MOVE_SPEED
            self.handle_collision_x(platforms)
            self.direction = "right"
            self.animate(self.spritesheet_right)
        else:
            # Установка статического изображения, если игрок не двигается
            if self.direction == "right":
                self.image = self.image_stand_right
            else:
                self.image = self.image_stand_left

    def animate(self, spritesheet):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame_index = (self.frame_index + 1) % 4  # Предполагаем 4 кадра в спрайтшите

        frame_width = spritesheet.get_width() // 4  # Предполагаем 4 кадра в спрайтшите
        frame_height = spritesheet.get_height()
        frame = spritesheet.subsurface(pygame.Rect(
            self.frame_index * frame_width, 0, frame_width, frame_height))
        self.image = pygame.transform.scale(frame, (40, 65))  # Масштабирование кадра до 40x65

    def check_collision_y(self, platforms):
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.y_velocity > 0:
                    self.rect.bottom = platform.rect.top
                    self.y_velocity = 0
                    self.on_ground = True
                elif self.y_velocity < 0:
                    self.rect.top = platform.rect.bottom
                    self.y_velocity = 0

        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            self.y_velocity = 0
            self.on_ground = True

    def handle_collision_x(self, platforms):
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.rect.right > platform.rect.left and self.rect.left < platform.rect.left:
                    self.rect.right = platform.rect.left
                elif self.rect.left < platform.rect.right and self.rect.right > platform.rect.right:
                    self.rect.left = platform.rect.right

    def check_collision_spikes(self, spikes):
        spike_hit_sound = pygame.mixer.Sound("resources/spike_hit.mp3")
        spike_hit_sound.set_volume(2)
        for spike in spikes:
            if self.rect.colliderect(spike.rect):
                self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
                self.y_velocity = 0
                self.on_ground = True
                self.spike_collision_time = pygame.time.get_ticks()
                self.control_disabled = True
                spike_hit_sound.play()
