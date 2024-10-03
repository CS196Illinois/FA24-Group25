import pygame
import math
import random

from pygame.constants import (
    K_UP,
    K_DOWN,
    K_s,
    K_w
)
# from random import randint

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 500
FONT = pygame.font.get_default_font()
SCORE = pygame.USEREVENT + 1

class GameState:
    p1score = 0
    p2score = 0
    reset = False

    @staticmethod
    def score(player):
        if player == 1:
            GameState.p1score += 1
        else:
            GameState.p2score += 1

        event = pygame.event.Event(SCORE)
        pygame.event.post(event)

class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super(Ball, self).__init__()

        self.surf = pygame.Surface((15, 15))

        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect(center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2))

        self.speed = 500.0
        self.angle = math.pi + random.randint(0, 1) * math.pi
        self.x_vel = self.speed * math.cos(self.angle)
        self.y_vel = self.speed * math.sin(self.angle)
        self.locked = False

    def update(self, dt):
        self.rect.move_ip(self.x_vel * dt, self.y_vel * dt)
        if self.rect.left < 0:
            GameState.score(2)
        elif self.rect.right > SCREEN_WIDTH:
            GameState.score(1)
        if self.rect.top < 0:
            self.angle = math.atan2(-self.y_vel, self.x_vel)
            self.rect.top = 0
        if self.rect.bottom > SCREEN_HEIGHT:
            self.angle = math.atan2(-self.y_vel, self.x_vel)
            self.rect.bottom = SCREEN_HEIGHT

        self.x_vel = math.cos(self.angle) * self.speed
        self.y_vel = math.sin(self.angle) * self.speed

    def collide(self, paddles):
        for i in paddles:
            if i.rect.colliderect(self.rect):
                offset = (self.rect.y + self.rect.height - i.rect.y) / (i.rect.height + self.rect.height)
                self.x_vel *= -1
                phi = 0.25 * math.pi * (2 * offset - 1)
                self.y_vel= ball.speed * math.sin(phi)
                self.angle = math.atan2(self.y_vel, self.x_vel)

    def reset(self):
        self.angle = math.pi + random.randint(0, 1) * math.pi
        self.rect.centerx = int(SCREEN_WIDTH/2)
        self.rect.centery = int(SCREEN_HEIGHT/2)

class Paddle(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos, controls):
        super(Paddle, self).__init__()

        self.surf = pygame.Surface((10, 75))

        self.surf.fill((255,255,255))

        self.rect = self.surf.get_rect(center = (x_pos, y_pos))
        self.vel = 0
        self.initial_y = y_pos
        self.max_vel = 500

        self.controls = controls
        self.locked = False

    def update(self, pressed_keys, bally, ballx, dt):
        if len(self.controls) == 0 and ballx > 700:
            # Make overshoots possible on the part of the CPU
            if self.rect.top > bally:
                self.vel = -self.max_vel
            elif self.rect.bottom < bally:
                self.vel = self.max_vel
            else:
                self.vel = 0
        elif len(self.controls) == 2:
            if pressed_keys[self.controls[0]]:
                self.vel -= self.max_vel
            elif pressed_keys[self.controls[1]]:
                self.vel += self.max_vel
            else:
                self.vel = 0

            if self.vel > self.max_vel:
                self.vel = self.max_vel
            elif self.vel < -self.max_vel:
                self.vel = -self.max_vel

        self.rect.move_ip(0, self.vel * dt)

        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
        elif self.rect.top < 0:
            self.rect.top = 0

    def reset(self):
        self.vel = 0
        self.rect.centery = self.initial_y

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
    dt = clock.tick(60)/1000
