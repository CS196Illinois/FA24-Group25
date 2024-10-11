import pygame
import random
import math

# To-do:
# x- ball movement
# x- collision with paddle
# x- opposite side paddle
# x- adjust new angle according to where ball hits paddle
# - increase AND decrease speed for the angle (larger reference angle = higher speed)
# - score tracker
# - rounds/game over process
# - wait for key press (space?) to start
# - implement paddle accel so paddle slides a bit proportional to length of key press
# - bug fixes
#       - ball clips through paddle ~15% of the time due to unknown factors

from pygame.locals import (
    K_UP,
    K_DOWN,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600



class Paddle(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Paddle, self).__init__()
        self.surf = pygame.Surface((13, 80))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect(center=(x, y))

    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
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
        self.speed = 5

    def move(self, angle, speed):
        self.rect.move_ip(math.cos(angle) * speed, math.sin(angle) * speed)

    def find_speed(self):
        global angle
        if angle > 0 and angle < 90:
            reference_angle = angle
        elif angle > 90 and angle < 180:
            reference_angle = 180 - angle
        elif angle > 180 and angle < 270:
            reference_angle = angle - 180
        else:
            reference_angle = 360 - angle
        speed_mult = (90 / reference_angle) * .1
        self.speed += self.speed * speed_mult
        print(self.speed)

    def update(self):
        global angle
        if self.rect.top <= 0 or self.rect.bottom >= SCREEN_HEIGHT:
            angle = 360 - angle
        elif self.rect.left <= 0 or self.rect.right >= SCREEN_WIDTH:
            pygame.event.post(pygame.event.Event(GAME_OVER))
        self.move(math.radians(angle), self.speed)

    def collision(self, paddle):
        global angle
        if self.rect.left <= paddle.rect.right or self.rect.right >= paddle.rect.left:
            angle = 180 - angle
        paddle_length = paddle.rect.bottom - paddle.rect.top
        proximity = math.fabs((paddle_length / 2) - self.rect.bottom) / paddle_length
        angle *= proximity
        #self.find_speed()
        self.move(math.radians(angle), self.speed)



pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
angles = [random.randint(20, 70), random.randint(110, 160), random.randint(200, 250), random.randint(290,340)]
angle = angles[random.randint(0, 3)]
GAME_OVER = pygame.USEREVENT + 1

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
while running:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        elif event.type == QUIT:
            running = False
        elif event.type == GAME_OVER:
            running = False

    pressed_keys = pygame.key.get_pressed()
    paddle1.update(pressed_keys)
    paddle2.update(pressed_keys)
    ball.update()
    screen.fill((0, 0, 0))

    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)
    if pygame.sprite.spritecollideany(ball, paddles):
        ball.collision(paddle1)
    
    pygame.display.flip()
    clock.tick(90)

pygame.quit()