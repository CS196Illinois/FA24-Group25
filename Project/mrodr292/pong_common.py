import pygame
import math
import random

SCORE = pygame.USEREVENT + 1
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

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

    def collide(self, paddles, dt):
        for i in paddles:
            if i.rect.colliderect(self.rect):
                offset = (self.rect.y + self.rect.height - i.rect.y) / (i.rect.height + self.rect.height)
                self.x_vel *= -1
                self.rect.move_ip(self.x_vel*dt, -self.y_vel*dt)
                phi = 0.3 * math.pi * (2 * offset - 1)
                self.y_vel= self.speed * math.sin(phi)
                self.angle = math.atan2(self.y_vel, self.x_vel)
                self.speed *= 1.01

    def reset(self):
        self.speed = 500
        self.angle = math.pi + random.randint(0, 1) * math.pi
        self.rect.centerx = int(SCREEN_WIDTH/2)
        self.rect.centery = int(SCREEN_HEIGHT/2)

class Paddle(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos, controls, size=75, thresh = 700):
        super(Paddle, self).__init__()

        self.surf = pygame.Surface((10, size))

        self.surf.fill((255,255,255))

        self.rect = self.surf.get_rect(center = (x_pos, y_pos))
        self.vel = 0.0
        self.initial_y = y_pos
        self.max_vel = 500.0

        self.controls = controls
        self.locked = False
        self.thresh = thresh

    def update(self, pressed_keys, bally, ballx, dt):
        if len(self.controls) == 0 and ballx > self.thresh and ballx < self.rect.x:
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
