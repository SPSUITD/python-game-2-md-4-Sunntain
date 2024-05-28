import pygame


class Button(pygame.sprite.Sprite):
    def __init__(self,x, y, width, height, texture):
        super().__init__()
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        button_texture = pygame.image.load(texture).convert_alpha()
        self.image.blit(button_texture, (0, 0))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.font = pygame.font.Font(None, 36)

    def update(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(pygame.mouse.get_pos()):
            return True
        return False