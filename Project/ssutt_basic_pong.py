import pygame
import random
import math

# To-do:
#
# x- ball movement
# x- collision with paddle
# x- opposite side paddle
# x- adjust new angle according to where ball hits paddle
# x- increase/decrease speed for the angle (larger reference angle = higher speed)
# x- score tracker/game over
# - wait for key press (space?) to start
# - implement paddle accel so paddle slides a bit proportional to length of key press
# x- bug fixes
#       x- ball clips through paddle ~15% of the time due to unknown factors

from pygame.locals import (
    K_UP,
    K_DOWN,
    K_ESCAPE,
    K_SPACE,
    K_w,
    K_s,
    KEYDOWN,
    QUIT,
)
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 550
SPEED = 6



class Paddle(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Paddle, self).__init__()
        self.surf = pygame.Surface((13, 80))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect(center=(x, y))

    def update(self, pressed_keys):
        if pressed_keys[K_w] and self == paddle1:
            self.rect.move_ip(0, -8)
        if pressed_keys[K_s] and self == paddle1:
            self.rect.move_ip(0, 8)      
        if pressed_keys[K_UP] and self == paddle2:
            self.rect.move_ip(0, -8)
        if pressed_keys[K_DOWN] and self == paddle2:
            self.rect.move_ip(0, 8)      
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super(Ball, self).__init__()
        self.surf = pygame.Surface((11, 11))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
        self.speed = SPEED

    def move(self, angle, speed):
        self.rect.move_ip(math.cos(angle) * speed, math.sin(angle) * speed)

    def update(self):
        global angle
        if self.rect.top <= 0 or self.rect.bottom >= SCREEN_HEIGHT:
            angle = 360 - angle
            print(angle)
        self.move(math.radians(angle), self.speed)

    def update_speed(self):
        global angle
        ref_angle = angle
        if angle > 90 and angle < 180:
            ref_angle = 180 - angle
        elif angle > 180 and angle < 270:
            ref_angle -= 180
        elif angle > 270 and angle < 360:
            ref_angle = 360 - angle
        multiplier = (90 / ref_angle) * 0.1
        self.speed = SPEED + (SPEED * multiplier)

    def collision(self, paddle):
        self.surf.fill((random.randint(25, 255), random.randint(25, 255), random.randint(25, 255)))
        global angle
        if self.rect.left <= paddle.rect.right or self.rect.right >= paddle.rect.left:
            angle = 180 - angle
        paddle_center = (paddle.rect.bottom - paddle.rect.top) / 2
        center_dist = paddle_center - self.rect.top
        angle = angle + (angle * (1 / center_dist))
        self.update_speed()
        self.move(math.radians(angle), self.speed)

def update_UI(ball):
    global score1_text
    global score2_text
    global score1
    global score2
    if ball.rect.left <= 0:
        score1 += 1
        score2_text = my_font.render(str(score1), False, (255, 255, 255))
        restart()
    elif ball.rect.right >= SCREEN_WIDTH:
        score2 += 1
        score1_text = my_font.render(str(score2), False, (255, 255, 255))
        restart()

def restart():
    global angles
    global angle
    global ball
    global paddle1
    global paddle2
    angles = [random.randint(20, 70), random.randint(110, 160), random.randint(200, 250), random.randint(290,340)]
    angle = angles[random.randint(0, 3)]
    ball.rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    paddle1.rect.center = (45, SCREEN_HEIGHT / 2)
    paddle2.rect.center = (SCREEN_WIDTH - 45, SCREEN_HEIGHT / 2)


pygame.init()
pygame.font.init()

my_font = pygame.font.SysFont('consolas', 80)
score1 = 0
score2 = 0
score1_text = my_font.render(str(score1), False, (255, 255, 255))
score2_text = my_font.render(str(score2), False, (255, 255, 255))
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
angles = [random.randint(20, 70), random.randint(110, 160), random.randint(200, 250), random.randint(290,340)]
angle = angles[random.randint(0, 3)]

paddle1 = Paddle(45, SCREEN_HEIGHT / 2)
paddle2 = Paddle(SCREEN_WIDTH - 45, SCREEN_HEIGHT / 2)
ball = Ball()
all_sprites = pygame.sprite.Group()
paddles = pygame.sprite.Group()

paddles.add(paddle1)
paddles.add(paddle2)
all_sprites.add(paddle2)
all_sprites.add(paddle1)
all_sprites.add(ball)

clock = pygame.time.Clock()
running = True
start = False
while running:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        elif event.type == QUIT:
            running = False

    pressed_keys = pygame.key.get_pressed()
    paddle1.update(pressed_keys)
    paddle2.update(pressed_keys)
    ball.update()
    update_UI(ball)
    screen.fill((0, 0, 0))

    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)
    screen.blit(score1_text, ((SCREEN_WIDTH / 2) - 80, 20))
    screen.blit(score2_text, ((SCREEN_WIDTH / 2) + 80, 20))
    
    if pygame.sprite.spritecollideany(ball, paddles):
        if (ball.rect.colliderect(paddle1)):
            ball.collision(paddle1)
        else:
            ball.collision(paddle2)
    
    pygame.display.flip()
    clock.tick(90)

pygame.quit()