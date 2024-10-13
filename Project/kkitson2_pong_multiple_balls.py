import pygame
import random

pygame.init()

#initials
WIDTH, HEIGHT = 1000, 600
wn = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong with Three Balls")
run = True

#colors
BLUE = (0, 0, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

#balls
radius = 15
num_balls = 3
balls = []

#initialize balls
for _ in range(num_balls):
    ball_x = random.randint(radius, WIDTH - radius)
    ball_y = random.randint(radius, HEIGHT - radius)
    ball_vel_x = random.choice([-0.7, 0.7])
    ball_vel_y = random.choice([-0.7, 0.7])
    balls.append([ball_x, ball_y, ball_vel_x, ball_vel_y])

#paddles
paddle_width, paddle_height = 20, 120
left_paddle_y = right_paddle_y = HEIGHT/2 - paddle_height/2
left_paddle_x, right_paddle_x = 100 - paddle_width/2, WIDTH - (100 - paddle_width/2)
right_paddle_vel = left_paddle_vel = 0

#main
while run:
    wn.fill(BLACK)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                right_paddle_vel = -0.9
            if event.key == pygame.K_DOWN:
                right_paddle_vel = 0.9
            if event.key == pygame.K_w:
                left_paddle_vel = -0.9
            if event.key == pygame.K_s:
                left_paddle_vel = 0.9
        elif event.type == pygame.KEYUP:
            if event.key in (pygame.K_UP, pygame.K_DOWN):
                right_paddle_vel = 0
            if event.key in (pygame.K_w, pygame.K_s):
                left_paddle_vel = 0

    #ball position
    for ball in balls:
        ball_x, ball_y, ball_vel_x, ball_vel_y = ball
        
        #ball movement
        ball_x += ball_vel_x
        ball_y += ball_vel_y

        #ball collision
        if ball_y <= radius or ball_y >= HEIGHT - radius:
            ball_vel_y *= -1
        
        #ball boundaries
        if ball_x >= WIDTH - radius or ball_x <= radius:
            ball_x = random.randint(radius, WIDTH - radius)
            ball_y = random.randint(radius, HEIGHT - radius)
            ball_vel_x = random.choice([-0.7, 0.7])
            ball_vel_y = random.choice([-0.7, 0.7])

        #paddle collision
        if left_paddle_x <= ball_x <= left_paddle_x + paddle_width:
            if left_paddle_y <= ball_y <= left_paddle_y + paddle_height:
                ball_x = left_paddle_x + paddle_width
                ball_vel_x *= -1

        if right_paddle_x <= ball_x <= right_paddle_x + paddle_width:
            if right_paddle_y <= ball_y <= right_paddle_y + paddle_height:
                ball_x = right_paddle_x - radius
                ball_vel_x *= -1

        #update balls
        ball[0], ball[1], ball[2], ball[3] = ball_x, ball_y, ball_vel_x, ball_vel_y

    #paddle boundaries
    left_paddle_y = max(0, min(left_paddle_y + left_paddle_vel, HEIGHT - paddle_height))
    right_paddle_y = max(0, min(right_paddle_y + right_paddle_vel, HEIGHT - paddle_height))

    #objects
    for ball in balls:
        pygame.draw.circle(wn, BLUE, (int(ball[0]), int(ball[1])), radius)
    
    pygame.draw.rect(wn, RED, (left_paddle_x, left_paddle_y, paddle_width, paddle_height))
    pygame.draw.rect(wn, RED, (right_paddle_x, right_paddle_y, paddle_width, paddle_height))

    pygame.display.update()

pygame.quit()
