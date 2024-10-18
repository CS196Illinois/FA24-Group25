# Simple pygame program

# Import and initialize the pygame library
import pygame
import pygame.draw_py
import pygame.freetype

pygame.init()

#colors
BLUE = (0,0,255)
BLACK = (0,0,0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

#Screen dimensions
WIDTH = 800
HEIGHT = 500

# Set up the drawing window
screen = pygame.display.set_mode([WIDTH, HEIGHT])

#fullscreen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
#screen = pygame.Surface((WIDTH, HEIGHT))

#In main loop before display.flip():

clock = pygame.time.Clock()
fps = 50
'''
class Obstacle(pygame.sprite.Sprite):
    def __init__(self, xLoc, yLoc, width, color):
        super().__init__()

        self.image = pygame.Surface([width, width])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)

        pygame.draw.rect(self.image, color, pygame.Rect(0, 0, width, width))
        self.rect = self.image.get_rect()
        self.rect.x = xLoc
        self.rect.y = yLoc

        def draw(self, surface):
            surface.blit(self.image, self.rect)
'''
class Ball(pygame.sprite.Sprite):
    def __init__(self, color, radius, xLoc, yLoc):
        super().__init__()

        self.image = pygame.Surface([radius * 2, radius * 2], pygame.SRCALPHA)
        self.image.fill((0, 0, 0, 0))  # Fill with transparent color

        pygame.draw.circle(self.image, color, (radius, radius), radius)  # Center the circle
        self.rect = self.image.get_rect()  # Correctly get the rectangle of the surface
        self.rect.x = float(xLoc)
        self.rect.y = float(yLoc)

        self.dy = 0
        self.dx = 5
        #change the entire how we are moving the ball   

    def toMove(self):
        self.rect.x += float(self.dx)   # Update rect position horizontally
        self.rect.y += float(self.dy)  # Update rect position vertically

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class Paddle(pygame.sprite.Sprite):
    def __init__(self, color, width, height, yLoc, xLoc):
        super().__init__()
        
        self.image = pygame.Surface([width, height])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)

        pygame.draw.rect(self.image, color, pygame.Rect(0, 0, width, height))
        self.rect = self.image.get_rect()
        self.rect.y = yLoc  # Set the initial y position of the paddle
        self.rect.x = xLoc

        self.dy = 7  # Paddle movement speed

    def toMove(self):
        self.rect.y += self.dy  # Update rect position directly

    def toMoveDown(self):
        self.rect.y -= self.dy

    def draw(self, surface):
        surface.blit(self.image, self.rect)

Paddle1 = Paddle(BLUE, 15, 90.0, 218.0, 20)
Paddle2 = Paddle(RED, 15, 90.0, 218.0, 760)
PingPong = Ball(WHITE, 10, 350.0, 250.0)
#Obstacle1 = Obstacle(200, 50, 10, WHITE)
# Run until the user asks to quit
running = True
playerOneScore = 0
playerTwoScore = 0
playerBall = True #tells whose turn it is, true means player 2; false means player 1
while running:
    clock.tick(fps)
    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the background with white
    screen.fill((0, 0, 0))

    #Text and score on top
    text = str(playerOneScore) + " | " + str(playerTwoScore)
    font = pygame.font.SysFont(None, 30);
    img = font.render(text, True, WHITE)
    screen.blit(img, (380, 20))

    # Ping pong ball and score keeping
    PingPong.toMove()


    #make game restart when it hits left and right 
    if PingPong.rect.top < 0:
        PingPong.dy *= -1
    if PingPong.rect.bottom > screen.get_height():
        PingPong.dy *= -1
    if PingPong.rect.left < 0:
        PingPong.dx = -5
        PingPong.dy = 0
        playerTwoScore += 1
        PingPong.rect.x = 350
        PingPong.rect.y = 250
    if PingPong.rect.right > screen.get_width():
        PingPong.dx = 5
        PingPong.dy = 0
        playerOneScore += 1
        PingPong.rect.x = 350
        PingPong.rect.y = 250

    #user inputs for both paddles
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        Paddle1.toMoveDown()  # Move up
    if keys[pygame.K_s]:
        Paddle1.toMove()   # Move down
    if keys[pygame.K_UP]:
        Paddle2.toMoveDown()  # Move up
    if keys[pygame.K_DOWN]:
        Paddle2.toMove()   # Move down
    
    if Paddle1.rect.top < 0:
        Paddle1.rect.top = 0
    if Paddle1.rect.bottom > screen.get_height():
        Paddle1.rect.bottom = screen.get_height()

    if Paddle2.rect.top < 0:
        Paddle2.rect.top = 0
    if Paddle2.rect.bottom > screen.get_height():
        Paddle2.rect.bottom = screen.get_height()
    
    if pygame.sprite.collide_rect(Paddle1, PingPong):
        distanceFromTop = Paddle1.rect.bottom - PingPong.rect.centery
        if distanceFromTop <= 15:
            PingPong.dy = 7
        elif distanceFromTop <= 25:
            PingPong.dy = 5
        elif distanceFromTop <= 33:
            PingPong.dy = 4
        elif distanceFromTop <= 41:
            PingPong.dy = 2
        elif distanceFromTop <= 49:
            PingPong.dy = 0
        elif distanceFromTop <= 57:
            PingPong.dy = -2
        elif distanceFromTop <= 65:
            PingPong.dy = -4
        elif distanceFromTop <= 75:
            PingPong.dy = -5
        else:   
            PingPong.dy = -7
        PingPong.dx *= -1
        PingPong.image.fill(BLUE)
        playerBall = False

    if pygame.sprite.collide_rect(PingPong, Paddle2):
        distanceFromTop = Paddle2.rect.bottom - PingPong.rect.centery
        if distanceFromTop <= 15:
            PingPong.dy = 9
        elif distanceFromTop <= 25:
            PingPong.dy = 7
        elif distanceFromTop <= 33:
            PingPong.dy = 3
        elif distanceFromTop <= 41:
            PingPong.dy = 2
        elif distanceFromTop <= 49:
            PingPong.dy = 0
        elif distanceFromTop <= 57:
            PingPong.dy = -2
        elif distanceFromTop <= 65:
            PingPong.dy = -3
        elif distanceFromTop <= 75:
            PingPong.dy = -7
        else:   
            PingPong.dy = -9
        PingPong.dx *= -1
        PingPong.image.fill(RED)
        playerBall = True
    
    Paddle1.draw(screen)
    Paddle2.draw(screen)
    PingPong.draw(screen)
    #Obstacle1.draw(screen)

    #scaled = pygame.transform.smoothscale(screen, fullscreen.get_size())
    #fullscreen.blit(scaled, (0, 0))
    # Flip the display
    pygame.display.flip()

# Done! Time to quit.
pygame.quit()