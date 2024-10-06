class Ball:
    def __init__(self, posX, posY, velX, velY, width, height, image):
        self.velX = velX
        self.velY = velY
        self.sprite = pygame.transform.scale(pygame.image.load(image).convert(), (width,height))
        self.rect = self.sprite.get_rect(center = (posX, posY))
        ballList.append(self)

    def checkCollision(self):
        if self.rect.top < 0 or self.rect.bottom > resY:
            self.velY *= -1
        if self.rect.collideobjects(paddleList) != None:
            self.velX *= -1.1
            self.velY += (self.rect.centery - self.rect.collideobjects(paddleList).rect.centery) * .03
    
    def updatePos(self):
        self.rect.centerx += self.velX
        self.rect.centery += self.velY

    def reset(self, posX, posY, velX, velY):
        self.velX = velX
        self.velY = velY
        self.rect.center = (posX,posY)

    def display(self):
        screen.blit(self.sprite, self.rect)


class Paddle:
    def __init__(self, posX, posY, width, height, speed, keyUp, keyDown, image):
        self.speed = abs(speed)
        self.sprite = pygame.transform.scale(pygame.image.load(image).convert(), (width,height))
        self.rect = self.sprite.get_rect(center = (posX,posY))
        self.keyUp = keyUp
        self.keyDown = keyDown
        paddleList.append(self)

    def getRect(self):
        return self.rect

    def updatePos(self):
        keys = pygame.key.get_pressed()
        if keys[self.keyUp]:
            self.rect.centery -= self.speed
        if keys[self.keyDown]:
            self.rect.centery += self.speed
        if self.rect.top < 0:
            self.rect.top = 0
        elif self.rect.bottom > resY:
            self.rect.bottom = resY

    def display(self):
        screen.blit(self.sprite, self.rect)

import pygame
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

background = pygame.image.load('graphics/background.png').convert()
background = pygame.transform.scale(background, (resX,resY))

ball = dict()
for i in range(0,1):
    ball[i] = Ball(resX * .5, resY * .5, 4, 0, 16, 16, 'graphics/ball.png')

paddleL = Paddle(resX * .03, resY * .5, resX * .015, resY * .25, 6, pygame.K_w, pygame.K_s, 'graphics/paddle.png')
paddleR = Paddle(resX * .97, resY * .5, resX * .015, resY * .25, 6, pygame.K_UP, pygame.K_DOWN, 'graphics/paddle.png')

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()
    
    textL = font.render(str(scoreL), True, 'White')
    textRectL = textL.get_rect(center = (resX * .4, resY * .1))
    textR = font.render(str(scoreR), True, 'White')
    textRectR = textR.get_rect(center = (resX * .6, resY * .1))

    screen.blit(background, (0,0))
    screen.blit(textL, textRectL)
    screen.blit(textR, textRectR)
    
    for ball in ballList:
        ball.checkCollision()
        if ball.rect.left < 0:
            scoreR += 1
            ball.reset(resX * .5, resY * .5, -4, 0)
        if ball.rect.right > resX:
            scoreL += 1
            ball.reset(resX * .5, resY * .5, 4, 0)
    
    for ball in ballList:
        ball.updatePos()
        ball.display()
    
    for paddle in paddleList:
        paddle.updatePos()
        paddle.display()

    pygame.display.update()
    clock.tick(60)