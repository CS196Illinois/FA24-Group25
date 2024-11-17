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

<<<<<<< HEAD
class SelectMenuButton(MenuButton):
    def __init__(self, x, y, action, text, input_param):
        super().__init__(x, y, action, text)
        self.input_param = input_param # in the case of music pong, this extra parameter is an int referring to the song to play
=======

class ControlsButton(MenuButton):
    def __init__(self, x, y, action, player):
        super().__init__(x, y, action, "")
        self.player = player

        if player == 1:
            self.state = "W/S"
        else:
            self.state = "None"

        self.text = f"Player {self.player}: {self.state}"

>>>>>>> 168ee18 (add changing controls button)
    def check_click(self, x, y, settings):
        if (
            x <= self.rect.right
            and x >= self.rect.left
            and y <= self.rect.bottom
            and y >= self.rect.top
        ):
<<<<<<< HEAD
            self.action(settings, self.input_param)
            settings.screen.fill((0, 0, 0))
=======
            self.action(settings, self.next_controls(), self.player)
            self.text = f"Player {self.player}: {self.state}"

    def next_controls(self):
        if self.state == "W/S":
            self.state = "Arrows"
            return (pygame.K_UP, pygame.K_DOWN)
        elif self.state == "Arrows":
            self.state = "None"
            return ()
        elif self.state == "None":
            self.state = "W/S"
            return (pygame.K_w, pygame.K_s)


def change_controls(settings: Settings, new, player):
    if player == 1:
        settings.p1_controls = new
    else:
        settings.p2_controls = new


# def change_controls(settings: Settings, new, player):
#     if player == 1:
#         if new == "w/s":
#             settings.p1_controls = (pygame.K_w, pygame.K_s)
#         elif new == "u/d":
#             settings.p1_controls = (pygame.K_UP, pygame.K_DOWN)
#     else:
#         if new == "w/s":
#             settings.p2_controls = (pygame.K_w, pygame.K_s)
#         elif new == "u/d":
#             settings.p2_controls = (pygame.K_UP, pygame.K_DOWN)
#         else:
#             settings.p2_controls =
>>>>>>> 168ee18 (add changing controls button)
