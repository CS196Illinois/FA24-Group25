import pygame
import math
import random
from pong_common import GameState, Ball, Paddle, SCREEN_HEIGHT, SCREEN_WIDTH, SCORE

FONT = pygame.font.get_default_font()

# reset balls with random positions & velocities
def reset_balls(balls):
    positions = [
        (SCREEN_WIDTH / 3, SCREEN_HEIGHT / 2),
        (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3),
        (SCREEN_WIDTH * 2 / 3, SCREEN_HEIGHT * 2 / 3)
    ]
    
    for i, ball in enumerate(balls):
        ball.rect.center = positions[i]
        
        angle_choice = random.randint(0, 1) * math.pi + (math.pi / 3)
        if random.random() < 0.5:
            angle_choice = -angle_choice
        
        ball.angle = angle_choice
        ball.x_vel = ball.speed * math.cos(ball.angle)
        ball.y_vel = ball.speed * math.sin(ball.angle)

# reset paddles to center
def reset_paddles(player, player2):
    player.rect.centery = SCREEN_HEIGHT / 2
    player2.rect.centery = SCREEN_HEIGHT / 2

# ai movement
def ai_move(player2, balls, dt):
    ball = balls[0]
    ball_y = ball.rect.centery
    ball_y_velocity = ball.y_vel

    # predict ball's y position
    predicted_y = ball_y + (ball_y_velocity * SCREEN_HEIGHT / 2)
    predicted_y = max(min(predicted_y, SCREEN_HEIGHT - player2.rect.height / 2), player2.rect.height / 2)

    # move ai to prediction
    if player2.rect.centery < predicted_y:
        player2.vel = player2.max_vel
    elif player2.rect.centery > predicted_y:
        player2.vel = -player2.max_vel
    else:
        player2.vel = 0

def run(settings):
    running = True
    state = GameState()

    # balls
    balls = [
        Ball((255, 0, 0), None),
        Ball((0, 255, 0), None),
        Ball((0, 0, 255), None)
    ]
    
    reset_balls(balls)

    player = Paddle(SCREEN_WIDTH / 10, SCREEN_HEIGHT / 2, settings.p1_controls)
    player2 = Paddle((SCREEN_WIDTH * 9) / 10, SCREEN_HEIGHT / 2, settings.p2_controls)
    score = pygame.font.Font(FONT, 20)
    score_text = score.render(
        f"{state.p1score} - {state.p2score}", False, (255, 255, 255)
    )

    clock = pygame.time.Clock()

    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)
    all_sprites.add(player2)
    for ball in balls:
        all_sprites.add(ball)

    paddles = pygame.sprite.Group()
    paddles.add(player)
    paddles.add(player2)

    dt = 0

    while running:
        settings.screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == SCORE:
                score_text = score.render(
                    f"{state.p1score} - {state.p2score}", False, (255, 255, 255)
                )
                reset_balls(balls)
                reset_paddles(player, player2)

        if state.p2score > 5 or state.p1score > 5:
            running = False

        for ball in balls:
            ball.update(dt, state)
            ball.collide(paddles, dt)

            # ball-to-ball collision
            for other_ball in balls:
                if ball != other_ball and ball.rect.colliderect(other_ball.rect):
                    offset_x = ball.rect.centerx - other_ball.rect.centerx
                    offset_y = ball.rect.centery - other_ball.rect.centery
                    overlap_distance = max(abs(offset_x), abs(offset_y))
                    if overlap_distance < 2:
                        overlap_distance = 2
                    ball.rect.move_ip(offset_x / overlap_distance, offset_y / overlap_distance)
                    other_ball.rect.move_ip(-offset_x / overlap_distance, -offset_y / overlap_distance)

                    ball.x_vel, other_ball.x_vel = other_ball.x_vel, ball.x_vel
                    ball.y_vel, other_ball.y_vel = other_ball.y_vel, ball.y_vel

        if len(player2.controls) == 0:
            ai_move(player2, balls, dt)

        keys = pygame.key.get_pressed()

        for paddle in paddles:
            paddle.update(keys, balls[0].rect.centery, balls[0].rect.centerx, dt)

        for entity in all_sprites:
            settings.screen.blit(entity.surf, entity.rect)

        settings.screen.blit(
            score_text, ((int(SCREEN_WIDTH / 2), (SCREEN_HEIGHT * 9) / 10))
        )

        pygame.display.flip()
        dt = clock.tick(120) / 1000.0