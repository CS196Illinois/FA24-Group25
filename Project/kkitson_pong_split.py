import pygame
import random
import math
from pong_common import GameState, Ball, Paddle, SCREEN_HEIGHT, SCREEN_WIDTH, SCORE

FONT = pygame.font.get_default_font()

# reset balls
def reset_balls(balls):
    positions = [(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)]
    
    for ball in balls:
        ball.rect.center = positions[0]
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
    predicted_y = ball_y + ball_y_velocity * (SCREEN_HEIGHT / 2) * dt
    predicted_y = max(min(predicted_y, SCREEN_HEIGHT - player2.rect.height / 2), player2.rect.height / 2)

    if player2.rect.centery < predicted_y:
        player2.vel = player2.max_vel
    elif player2.rect.centery > predicted_y:
        player2.vel = -player2.max_vel
    else:
        player2.vel = 0

def run(settings):
    running = True
    state = GameState()
    ball = Ball((255, 255, 255), None)
    balls = [ball]

    player = Paddle(SCREEN_WIDTH / 10, SCREEN_HEIGHT / 2, settings.p1_controls)
    player2 = Paddle((SCREEN_WIDTH * 9) / 10, SCREEN_HEIGHT / 2, settings.p2_controls)
    score = pygame.font.Font(FONT, 20)
    score_text = score.render(f"{state.p1score} - {state.p2score}", False, (255, 255, 255))

    clock = pygame.time.Clock()

    all_sprites = pygame.sprite.Group()
    all_sprites.add(player, player2, ball)

    paddles = pygame.sprite.Group()
    paddles.add(player, player2)

    dt = 0
    paddle_hits = 0

    while running:
        settings.screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == SCORE:
                score_text = score.render(f"{state.p1score} - {state.p2score}", False, (255, 255, 255))
                for entity in all_sprites:
                    entity.reset()

                paddle_hits = 0
                balls = [ball]
                all_sprites = pygame.sprite.Group()
                all_sprites.add(ball, player, player2)
                ball.reset()

        if state.p2score > 5 or state.p1score > 5:
            running = False

        for ball in balls[:]:
            ball.update(dt, state)

            # count paddle hits
            if ball.rect.colliderect(player.rect) or ball.rect.colliderect(player2.rect):
                paddle_hits += 1

                # split the ball after multiple paddle hits
                if paddle_hits >= random.randint(1, 3) and len(balls) == 1:
                    new_ball1 = Ball((255, 255, 255), None)
                    new_ball2 = Ball((255, 255, 255), None)

                    new_ball1.rect.center = ball.rect.center
                    new_ball2.rect.center = ball.rect.center

                    if ball.rect.centerx < SCREEN_WIDTH / 2:
                        angle1 = random.uniform(math.pi / 4, 3 * math.pi / 4)
                        angle2 = random.uniform(math.pi / 4, 3 * math.pi / 4)
                    else:
                        angle1 = random.uniform(-3 * math.pi / 4, -math.pi / 4)
                        angle2 = random.uniform(-3 * math.pi / 4, -math.pi / 4)

                    new_ball1.x_vel = math.cos(angle1) * new_ball1.speed
                    new_ball1.y_vel = math.sin(angle1) * new_ball1.speed

                    new_ball2.x_vel = math.cos(angle2) * new_ball2.speed
                    new_ball2.y_vel = math.sin(angle2) * new_ball2.speed

                    balls.append(new_ball1)
                    balls.append(new_ball2)
                    all_sprites.add(new_ball1)
                    all_sprites.add(new_ball2)

                    paddle_hits = 0
                    all_sprites.remove(ball)
                    balls.remove(ball)

                    break

            ball.collide(paddles, dt)

            # ball-to-ball collision
            for other_ball in balls:
                if ball != other_ball and ball.rect.colliderect(other_ball.rect):
                    offset_x = ball.rect.centerx - other_ball.rect.centerx
                    offset_y = ball.rect.centery - other_ball.rect.centery
                    distance = math.sqrt(offset_x**2 + offset_y**2)
                    if distance == 0:
                        continue
                    
                    norm_x = offset_x / distance
                    norm_y = offset_y / distance
                    move_distance = 2
                    ball.rect.move_ip(norm_x * move_distance, norm_y * move_distance)
                    other_ball.rect.move_ip(-norm_x * move_distance, -norm_y * move_distance)

                    angle_ball = math.atan2(ball.y_vel, ball.x_vel)
                    angle_other_ball = math.atan2(other_ball.y_vel, other_ball.x_vel)

                    ball.x_vel = math.cos(angle_ball + math.pi) * ball.speed
                    ball.y_vel = math.sin(angle_ball + math.pi) * ball.speed

                    other_ball.x_vel = math.cos(angle_other_ball + math.pi) * other_ball.speed
                    other_ball.y_vel = math.sin(angle_other_ball + math.pi) * other_ball.speed

        if len(player2.controls) == 0:
            ai_move(player2, balls, dt)

        keys = pygame.key.get_pressed()
        for paddle in paddles:
            paddle.update(keys, ball.rect.centery, ball.rect.centerx, dt)

        for entity in all_sprites:
            settings.screen.blit(entity.surf, entity.rect)

        settings.screen.blit(
            score_text, ((int(SCREEN_WIDTH / 2), (SCREEN_HEIGHT * 9) / 10))
        )

        pygame.display.flip()
        dt = clock.tick(120) / 1000.0