# Simple pygame program

# Import and initialize the pygame library
import pygame
import pygame.draw_py
import pygame.freetype

pygame.init()

#colors
BLUE = (0,0,255)
BLACK = (0,0,0)

#Screen dimensions
WIDTH = 800
HEIGHT = 500

# Set up the drawing window
screen = pygame.display.set_mode([WIDTH, HEIGHT])

class Ball(pygame.sprite.Sprite):
    def __init__(self, color, radius, xLoc, yLoc):
        super().__init__()

        self.image = pygame.Surface([radius * 2, radius * 2], pygame.SRCALPHA)
        self.image.fill((0, 0, 0, 0))  # Fill with transparent color

        pygame.draw.circle(self.image, color, (radius, radius), radius)  # Center the circle
        self.rect = self.image.get_rect()  # Correctly get the rectangle of the surface
        self.rect.x = float(xLoc)
        self.rect.y = float(yLoc)

        self.dy = 0.6
        self.dx = 0.7
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

        self.dy = 0.7  # Paddle movement speed

    def toMove(self):
        self.rect.y += self.dy  # Update rect position directly

    def toMoveDown(self):
        self.rect.y -= self.dy

    def draw(self, surface):
        surface.blit(self.image, self.rect)

Paddle1 = Paddle(BLUE, 15, 70.0, 50.0, 20)
Paddle2 = Paddle(BLUE, 15, 70.0, 50.0, 780)
PingPong = Ball(BLUE, 5, 50.0, 50.0)
# Run until the user asks to quit
running = True
playerOneScore = 0
playerTwoScore = 0
while running:

    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the background with white
    screen.fill((255, 255, 255))

    #Text and score on top
    text = str(playerOneScore) + " | " + str(playerTwoScore)
    font = pygame.font.SysFont(None, 30);
    img = font.render(text, True, (0,0,255))
    screen.blit(img, (400, 20))

    # Ping pong ball and score keeping
    PingPong.toMove()


    #make game restart when it hits left and right 
    if PingPong.rect.top < 0:
        PingPong.dy *= -1
    if PingPong.rect.bottom > screen.get_height():
        PingPong.dy *= -1
    if PingPong.rect.left < 0:
        PingPong.dx *= -1
        playerTwoScore += 1
    if PingPong.rect.right > screen.get_width():
        PingPong.dx *= -1
        playerOneScore += 1

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
        PingPong.dx *= -1

    if pygame.sprite.collide_rect(PingPong, Paddle2):
        PingPong.dx *= -1
    

    Paddle1.draw(screen)
    Paddle2.draw(screen)
    PingPong.draw(screen)

    # Flip the display
    pygame.display.flip()

# Done! Time to quit.
pygame.quit()