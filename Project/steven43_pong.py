class Ball:
    def __init__(self, posX, posY, velX, velY, width, height, image):
        self.velX = velX
        self.velY = velY
        self.width = width
        self.height = height
        self.sprite = pygame.transform.scale(pygame.image.load(image).convert(), (width,height))
        self.rect = self.sprite.get_rect(center = (posX, posY))
        self.lastHit = None
        ballList.append(self)

    def checkCollision(self):
        if self.rect.top < 0 or self.rect.bottom > resY:
            self.velY *= -1
        if self.rect.collideobjects(paddleList) != None:
            self.lastHit = self.rect.collideobjects(paddleList)
            self.velX *= -1.05
            self.velY += (self.rect.centery - self.rect.collideobjects(paddleList).rect.centery) * .03
    
    # update ball position every frame
    def updatePos(self):
        self.rect.centerx += self.velX
        self.rect.centery += self.velY
        # pull implementation
        if self.lastHit != None and keys[self.lastHit.keyPull]:
            if self.lastHit.rect.centery > self.rect.centery:
                self.velY += .05
            if self.lastHit.rect.centery < self.rect.centery:
                self.velY -= .05

    def display(self):
        screen.blit(self.sprite, self.rect)
        # graphics for when ball is being pulled
        if self.lastHit and keys[self.lastHit.keyPull]:
            self.sprite = pygame.transform.scale(pygame.image.load('steven43_graphics/' + self.lastHit.name + 'ball.png').convert(), (self.width,self.height))
        else:
            self.sprite = pygame.transform.scale(pygame.image.load('steven43_graphics/ball.png').convert(), (self.width,self.height))

    def reset(self, posX, posY, velX, velY):
        self.velX = velX
        self.velY = velY
        self.rect.center = (posX,posY)
        self.lastHit = None
class Paddle:
    def __init__(self, posX, posY, width, height, speed, dashCooldownSeconds, keyUp, keyDown, keyDash, keyPull, name):
        self.speed = abs(speed)
        self.width = width
        self.height = height
        self.sprite = pygame.transform.scale(pygame.image.load('steven43_graphics/' + name + '.png').convert(), (width,height))
        self.rect = self.sprite.get_rect(center = (posX,posY))
        self.keyUp = keyUp
        self.keyDown = keyDown
        self.keyDash = keyDash
        self.keyPull = keyPull
        self.dashCooldownSeconds = dashCooldownSeconds
        self.timeSinceDash = dashCooldownSeconds
        self.name = name
        paddleList.append(self)

    def getRect(self):
        return self.rect

    # update paddle position every frame
    def updatePos(self):
        self.timeSinceDash += 1/60
        if keys[self.keyUp]:
            self.rect.centery -= self.speed
        if keys[self.keyDown]:
            self.rect.centery += self.speed
        # dash movement and cooldown implementation
        if self.timeSinceDash >= self.dashCooldownSeconds:
            if keys[self.keyDash]:
                if keys[self.keyUp]:
                    self.timeSinceDash = 0
                    self.rect.centery -= self.speed * 25
                elif keys[self.keyDown]:
                    self.timeSinceDash = 0
                    self.rect.centery += self.speed * 25
        if self.rect.top < 0:
            self.rect.top = 0
        elif self.rect.bottom > resY:
            self.rect.bottom = resY

    def display(self):
        screen.blit(self.sprite, self.rect)
        # graphics for when paddle is on dash cooldown or pulling
        if self.timeSinceDash < self.dashCooldownSeconds:
            if keys[self.keyPull]:
                self.sprite = pygame.transform.scale(pygame.image.load('steven43_graphics/' + self.name + 'cooldown.png').convert(), (self.width,self.height))
            else:
                self.sprite = pygame.transform.scale(pygame.image.load('steven43_graphics/paddlecooldown.png').convert(), (self.width,self.height))
        else:
            if keys[self.keyPull]:
                self.sprite = pygame.transform.scale(pygame.image.load('steven43_graphics/' + self.name + '.png').convert(), (self.width,self.height))
            else:
                self.sprite = pygame.transform.scale(pygame.image.load('steven43_graphics/paddle.png').convert(), (self.width,self.height))

import pygame
import random
from sys import exit

pygame.init()

resX = 960
resY = 540

ballList = []
paddleList = []
scoreL = 0
scoreR = 0
font = pygame.font.Font(None, 50)
screen = pygame.display.set_mode((resX,resY))
pygame.display.set_caption('pong')
clock = pygame.time.Clock()
font = pygame.font.Font(None, 50)

title = pygame.transform.scale(pygame.image.load('steven43_graphics/title.png').convert(), (resX,resY))
background = pygame.transform.scale(pygame.image.load('steven43_graphics/background.png').convert(), (resX,resY))

ball = dict()
for i in range(0,1):
    ball[i] = Ball(resX * .5, resY * .5, -4, 0, resX * .017, resX * .017, 'steven43_graphics/ball.png')


paddleL = Paddle(resX * .02, resY * .5, resX * .017, resY * .186, 6, 3, pygame.K_w, pygame.K_s, pygame.K_d, pygame.K_a, 'paddleL')
paddleR = Paddle(resX * .98, resY * .5, resX * .017, resY * .186, 6, 3, pygame.K_UP, pygame.K_DOWN, pygame.K_RIGHT, pygame.K_LEFT, 'paddleR')

start = False

while True:
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                start = True
                scoreL = 0
                scoreR = 0
                for ball in ballList:
                    ball.reset(resX * .5, resY * .5, -4, 0)
            if event.key == pygame.K_ESCAPE:
                start = False

    textL = font.render(str(scoreL), True, 'White')
    textRectL = textL.get_rect(center = (resX * .4, resY * .1))
    textR = font.render(str(scoreR), True, 'White')
    textRectR = textR.get_rect(center = (resX * .6, resY * .1))

    if start == False:
        screen.blit(title, (0,0))
    else:
        screen.blit(background, (0,0))
        screen.blit(textL, textRectL)
        screen.blit(textR, textRectR)
    
    for ball in ballList:
        ball.checkCollision()
        if ball.rect.left < resX * .02:
            scoreR += 1
            ball.reset(resX * .5, resY * .5, -4, 0)
        if ball.rect.right > resX * .98:
            scoreL += 1
            ball.reset(resX * .5, resY * .5, 4, 0)
    
    for paddle in paddleList:
        paddle.updatePos()

    for ball in ballList:
        ball.updatePos()
        ball.display()
    
    for paddle in paddleList:
        paddle.display()

    pygame.display.update()
    clock.tick(60)