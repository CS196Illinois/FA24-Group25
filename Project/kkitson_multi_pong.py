import pygame
from pygame.constants import K_UP, K_DOWN, K_s, K_w
import math

from pong_common import GameState, Ball, Paddle, SCREEN_HEIGHT, SCREEN_WIDTH, SCORE

FONT = pygame.font.get_default_font()

pygame.init()

def run(settings):
    running = True

    # initialize multiple balls
    balls = [Ball() for _ in range(3)]

    player = Paddle(SCREEN_WIDTH / 10, SCREEN_HEIGHT / 2, (K_w, K_s), size=60)
    player2 = Paddle((SCREEN_WIDTH * 4) / 10, SCREEN_HEIGHT / 2, (K_UP, K_DOWN), size=60)
    cpu1 = Paddle((SCREEN_WIDTH * 9) / 10, SCREEN_HEIGHT / 2, (), size=30, thresh=800)
    cpu2 = Paddle((SCREEN_WIDTH * 6) / 10, SCREEN_HEIGHT / 2, (), size=30, thresh=500)
    score = pygame.font.Font(FONT, 20)
    score_text = score.render(
        f"{GameState.p1score} - {GameState.p2score}", False, (255, 255, 255)
    )

    clock = pygame.time.Clock()

    all_sprites = pygame.sprite.Group(*balls, player, player2, cpu1, cpu2)
    paddles = pygame.sprite.Group(player, player2, cpu1, cpu2)

    dt = 0

    while running:
        settings.screen.fill((0, 128, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == SCORE:
                score_text = score.render(
                    f"{GameState.p1score} - {GameState.p2score}", False, (255, 255, 255)
                )
                for entity in all_sprites:
                    entity.reset()

        if GameState.p2score > 5 or GameState.p1score > 5:
            running = False
            GameState.reset()

        # update balls
        for i, ball in enumerate(balls):
            ball.update(dt)
            ball.collide(paddles, dt)
            
            # ball-to-ball collision
            for j, other_ball in enumerate(balls[i+1:], start=i+1):
                if ball.rect.colliderect(other_ball.rect):
                    ball.x_vel, other_ball.x_vel = other_ball.x_vel, ball.x_vel
                    ball.y_vel, other_ball.y_vel = other_ball.y_vel, ball.y_vel
                    ball.rect.move_ip(ball.x_vel * dt, ball.y_vel * dt)
                    other_ball.rect.move_ip(other_ball.x_vel * dt, other_ball.y_vel * dt)

        # update paddle positions based on closest ball
        keys = pygame.key.get_pressed()
        for paddle in paddles:
            closest_ball = min(balls, key=lambda b: abs(b.rect.centerx - paddle.rect.centerx))
            paddle.update(keys, closest_ball.rect.centery, closest_ball.rect.centerx, dt)

        for entity in all_sprites:
            settings.screen.blit(entity.surf, entity.rect)

        settings.screen.blit(
            score_text, ((int(SCREEN_WIDTH / 2), (SCREEN_HEIGHT * 9) / 10))
        )

        pygame.display.flip()
        dt = clock.tick(120) / 1000.0