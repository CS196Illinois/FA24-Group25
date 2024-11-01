import pygame
from pygame.surface import Surface


class Settings:
    def __init__(self, p1_ctrl, p2_ctrl, scrn):
        self.p1_controls = p1_ctrl
        self.p2_controls = p2_ctrl
        self.screen = scrn


class MenuButton(pygame.sprite.Sprite):
    def __init__(self, x, y, action, text):
        super().__init__()
        self.surf = Surface((150, 150))
        self.surf.fill((128, 128, 64))
        self.rect = self.surf.get_rect(center=(x, y))
        self.action = action
        self.text = text

    def check_click(self, x, y, settings):
        if (
            x <= self.rect.right
            and x >= self.rect.left
            and y <= self.rect.bottom
            and y >= self.rect.top
        ):
            self.action(settings)
            settings.screen.fill((0, 0, 0))
