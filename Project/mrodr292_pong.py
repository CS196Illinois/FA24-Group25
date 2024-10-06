import pygame
from pygame.constants import (
    K_UP,
    K_DOWN,
    K_s,
    K_w
)

from mrodr292_pong_entities import GameState, Ball, Paddle, SCREEN_HEIGHT, SCREEN_WIDTH, SCORE

FONT = pygame.font.get_default_font()

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

running = True

ball = Ball()
player = Paddle(SCREEN_WIDTH/10, SCREEN_HEIGHT/2, (K_UP, K_DOWN))
player2 = Paddle((SCREEN_WIDTH * 9)/10, SCREEN_HEIGHT/2, ())
score = pygame.font.Font(FONT, 20)
score_text = score.render(f"{GameState.p1score} - {GameState.p2score}", False, (255, 255, 255))

clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()
all_sprites.add(ball)
all_sprites.add(player)
all_sprites.add(player2)

paddles = pygame.sprite.Group()
paddles.add(player)
paddles.add(player2)

dt = 0

while running:
    screen.fill((0,0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == SCORE:
            score_text = score.render(f"{GameState.p1score} - {GameState.p2score}", False, (255, 255, 255))
            for entity in all_sprites:
                entity.reset()
    
    ball.update(dt)
    ball.collide(paddles)
    keys = pygame.key.get_pressed()

    for paddle in paddles:
        paddle.update(keys, ball.rect.centery, ball.rect.centerx, dt)

    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    screen.blit(score_text, ((int(SCREEN_WIDTH/2), (SCREEN_HEIGHT * 9)/10)))

    pygame.display.flip()
    dt = clock.tick(120)/1000.0
