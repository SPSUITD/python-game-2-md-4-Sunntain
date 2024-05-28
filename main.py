from button import *
from player import *
from platform import *
from key import *
from door import *
from spikes import *
from config import *
import pygame

# Инициализация Pygame
pygame.init()

# Загрузка фоновой музыки
pygame.mixer.music.load("resources/background_music.mp3")
pygame.mixer.music.set_volume(0.5)  # Установка громкости на 50%
pygame.mixer.music.play(-1)  # Зацикливание воспроизведения музыки

button_click_sound = pygame.mixer.Sound("resources/button_click.mp3")
key_pickup_sound = pygame.mixer.Sound("resources/key_pickup.mp3")

background_menu = pygame.image.load("resources/background_menu.png")
background_lv1 = pygame.image.load("resources/background_lv1.png")
background_lv2 = pygame.image.load("resources/background_lv2.png")

# Создание окна
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Сангвин и кристаллы судьбы")
lvl1_completed = False

# Функция отображения подсказки
def draw_tooltip(text, button_rect):
    font = pygame.font.Font("resources/ITP.ttf", 20)
    tooltip_text = font.render(text, True, BLUE)
    tooltip_rect = tooltip_text.get_rect()
    tooltip_rect.midbottom = button_rect.midtop  # Position tooltip above the button
    tooltip_rect.y -= 10  # Add a small margin above the button

    # Adjust tooltip position to keep it within screen bounds
    if tooltip_rect.right > SCREEN_WIDTH:
        tooltip_rect.right = SCREEN_WIDTH
    if tooltip_rect.left < 0:
        tooltip_rect.left = 0
    if tooltip_rect.top < 0:
        tooltip_rect.top = 0
    pygame.draw.rect(screen, PURPLE, tooltip_rect.inflate(10, 10))
    screen.blit(tooltip_text, tooltip_rect)

# Функция отображения главного меню
def main_menu():

    lvl1_button = Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 100, 200, 50, "resources/button_lv1.png")
    lvl2_button = Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2, 200, 50, "resources/button_lv2.png")
    quit_button = Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 100, 200, 50, "resources/button_exit.png")

    menu_sprites = pygame.sprite.Group(lvl1_button, lvl2_button, quit_button)

    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if lvl1_button.update(event):
                button_click_sound.play()
                return start_lvl1()
            if lvl2_button.update(event) and lvl1_completed:
                button_click_sound.play()
                return start_lvl2()
            if quit_button.update(event):
                button_click_sound.play()
                running = False
                pygame.quit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
                pygame.quit()

        if running:
            screen.blit(background_menu, (0, 0))
            menu_sprites.draw(screen)

            # Проверяем, наведена ли мышь на кнопку уровня 2
            if lvl2_button.rect.collidepoint(mouse_pos) and not lvl1_completed:
                draw_tooltip("Доступно только после прохождения уровня 1", lvl2_button.rect)

            pygame.display.flip()

# Функция для запуска уровня 1
def start_lvl1():
    # Создание игрока
    player = Player()

    # Создание списка платформ
    platforms = [
        Platform(10, 500, 100, 20),
        Platform(10, 300, 100, 20),
        Platform(130, 200, 100, 20),
        Platform(630, 110, 100, 20),
        Platform(675, 400, 100, 20),
        Platform(550, 300, 100, 20),
        Platform(700, 200, 100, 20),
    ]
    for i in range (0,900,100):
        platforms.append(Platform(i,590,100,20))
    # Создание списка шипов
    spikes = [
        Spike(250, 470, 30, 30),
        Spike(450, 370, 30, 30),
        Spike(700, 270, 30, 30)
    ]

    # Создание ключа
    key = Key(165, 145, 50, 50)

    # Создание двери
    door = Door(655, 10, 50, 100)

    all_sprites = pygame.sprite.Group()
    all_sprites.add(player, key)
    for platform in platforms:
        all_sprites.add(platform)
    for spike in spikes:
        all_sprites.add(spike)

    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                if main_menu():
                    pygame.quit()
                else:
                    main_menu()

        # Обновление игры
        player.update(platforms, spikes)
        key.update()  # Обновление анимации ключа
        for i in spikes:
            i.update()

        # Проверяем столкновение с ключом
        collided_sprites = pygame.sprite.spritecollide(player, all_sprites, False)
        if collided_sprites:
            for sprite in collided_sprites:
                if isinstance(sprite, Key):  # Проверяем, что столкнулись с ключом
                    player.has_key = True
                    all_sprites.remove(sprite)  # Удаляем ключ из группы спрайтов
                    all_sprites.add(door)
                    key_pickup_sound.play()

        # Проверяем столкновение с дверью
        if door.check_collision(player):
            global lvl1_completed
            # Выводим сообщение о победе
            lvl1_completed = True
            # Загрузка изображения уведомления о победе
            win_image = pygame.image.load("resources/win_lv1.png").convert_alpha()

            # Создаем прямоугольник для уведомления
            win_rect = win_image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

            # Отображаем уведомление на экране
            screen.blit(win_image, win_rect)
            pygame.display.flip()

            pygame.time.delay(2000)  # Задержка для отображения сообщения о победе
            main_menu()  # Возвращаемся в главное меню

        # Отрисовка экрана
        screen.blit(background_lv1, (0, 0))  # Отображаем фон уровня 1
        if not door.opened:
            for sprite in all_sprites:
                screen.blit(sprite.image, sprite.rect)
        pygame.display.flip()

        # Задержка для 60 кадров в секунду
        clock.tick(60)

# Функция для запуска уровня 2
def start_lvl2():
    # Создание игрока
    player = Player()

    # Создание списка платформ
    platforms = [
        Platform(10, 100, 100, 20),
        Platform(10, 500, 100, 20),
        Platform(10, 300, 100, 20),
        Platform(130, 200, 100, 20),
        Platform(675, 400, 100, 20),
        Platform(610, 200, 100, 20),
        Platform(350, 400, 100, 20)
    ]
    for i in range (0,900,100):
        platforms.append(Platform(i,590,100,20))

    # Создание списка шипов
    spikes = [
        Spike(450, 540, 30, 30),
        Spike(450, 440, 30, 30),
        Spike(450, 340, 30, 30),
        Spike(450, 240, 30, 30),
        Spike(450, 140, 30, 30),
        Spike(450, 40, 30, 30)
    ]

    # Создание ключа
    key = Key(713, 340, 50, 50)

    # Создание двери
    door = Door(630, 100, 50, 100)

    all_sprites = pygame.sprite.Group()
    all_sprites.add(player, key)
    for platform in platforms:
        all_sprites.add(platform)
    for spike in spikes:
        all_sprites.add(spike)

    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                if main_menu():
                    pygame.quit()
                else:
                    main_menu()

        # Обновление игры
        player.update(platforms, spikes)
        key.update()  # Обновление анимации ключа
        for i in spikes:
            i.update()

        # Проверяем столкновение с ключом
        collided_sprites = pygame.sprite.spritecollide(player, all_sprites, False)
        if collided_sprites:
            for sprite in collided_sprites:
                if isinstance(sprite, Key):  # Проверяем, что столкнулись с ключом
                    player.has_key = True
                    all_sprites.remove(sprite)  # Удаляем ключ из группы спрайтов
                    all_sprites.add(door)
                    key_pickup_sound.play()

        # Проверяем столкновение с дверью
        if door.check_collision(player):
            global lvl1_completed
            # Выводим сообщение о победе
            win_image = pygame.image.load("resources/win_lv2.png").convert_alpha()

            # Создаем прямоугольник для уведомления
            win_rect = win_image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

            # Отображаем уведомление на экране
            screen.blit(win_image, win_rect)
            pygame.display.flip()

            pygame.time.delay(2000)  # Задержка для отображения сообщения о победе
            main_menu()  # Возвращаемся в главное меню

        # Отрисовка экрана
        screen.blit(background_lv2, (0, 0))  # Отображаем фон уровня 2
        if not door.opened:
            for sprite in all_sprites:
                screen.blit(sprite.image, sprite.rect)
        pygame.display.flip()

        # Задержка для 60 кадров в секунду
        clock.tick(60)

main_menu()

# Завершение Pygame
pygame.quit()
