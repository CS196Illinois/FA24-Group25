import pygame
from pygame.constants import K_UP, K_DOWN, K_s, K_w
<<<<<<< HEAD
from menu import Settings, MenuButton, SelectMenuButton
=======
from menu import Settings, MenuButton, ControlsButton, change_controls
>>>>>>> 168ee18 (add changing controls button)
import mrodr292_pong
import mrodr292_foosball
<<<<<<< HEAD
import cmt8_musicpong
=======
import steven43_pong
>>>>>>> 2effa20 (initial commit with common.py, added menu button)
from pong_common import SCREEN_WIDTH, SCREEN_HEIGHT

FONT = pygame.font.get_default_font()

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
settings = Settings((K_w, K_s), (), screen)

pong_button = MenuButton(
    SCREEN_WIDTH / 3, (SCREEN_HEIGHT * 3) / 4, mrodr292_pong.run, "PONG!"
)
foosball_button = MenuButton(
    (SCREEN_WIDTH * 2) / 3, (SCREEN_HEIGHT * 3) / 4, mrodr292_foosball.run, "FOOSBALL!"
)
<<<<<<< HEAD
<<<<<<< HEAD
music_button = SelectMenuButton(
    (SCREEN_WIDTH * 2) / 3, (SCREEN_HEIGHT * 2) / 4, cmt8_musicpong.run, "MUSIC!", 0
=======
test_button = MenuButton(
    SCREEN_WIDTH / 3, SCREEN_HEIGHT / 4, steven43_pong.run, "test!"
>>>>>>> 2effa20 (initial commit with common.py, added menu button)
)
menu_group = pygame.sprite.Group()
menu_group.add(pong_button)
menu_group.add(foosball_button)
<<<<<<< HEAD
menu_group.add(music_button)
=======
menu_group.add(test_button)
>>>>>>> 2effa20 (initial commit with common.py, added menu button)
=======

p1_controls = ControlsButton(
    (SCREEN_WIDTH * 2) / 10, (SCREEN_HEIGHT * 2) / 10, change_controls, 1
)
p2_controls = ControlsButton(
    (SCREEN_WIDTH * 8) / 10, (SCREEN_HEIGHT * 2) / 10, change_controls, 2
)

menu_group = pygame.sprite.Group()
menu_group.add(pong_button)
menu_group.add(foosball_button)
menu_group.add(p1_controls)
menu_group.add(p2_controls)
>>>>>>> 168ee18 (add changing controls button)
font = pygame.font.Font(FONT, 20)
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                for button in menu_group:
                    button.check_click(mouse_x, mouse_y, settings)

    for button in menu_group:
        settings.screen.blit(button.surf, button.rect)
        settings.screen.blit(
            font.render(button.text, True, (255, 255, 255)),
            (button.rect.left + 10, button.rect.top + 10),
        )
    pygame.display.flip()
