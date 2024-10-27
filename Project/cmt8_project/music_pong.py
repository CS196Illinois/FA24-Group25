#Import pygame module
import pygame

import random

#Import pygame.locals to access keys easier
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    K_w,
    K_s,
    KEYDOWN,
    QUIT
)


#Define screen size (this will be scaled/stretched to be fullscreen later anyway)
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

#Music pong variables
distanceToNextPaddle = (SCREEN_WIDTH - 25) - (SCREEN_WIDTH / 2 + 5) # starting distance upon game launch


beatsPerMinute = 120
subdivision = 2 # 1: whole note subdivision, 2: half note subdivision, 4: quarter note subdivision and so on


#Define a Player object by extending pygame.sprite.Sprite
#The surface drawn on the screen is now an attribute of 'player'
class Player1(pygame.sprite.Sprite):

    def __init__(self):
        super(Player1, self).__init__()
        self.surf = pygame.Surface((15, 100))
        self.surf.fill((0, 0, 255))
        self.rect = self.surf.get_rect()

    # Move the sprite based on user keypresses
    def update(self, pressed_keys):
        if pressed_keys[K_w]:
            self.rect.move_ip(0, -7)
        if pressed_keys[K_s]:
            self.rect.move_ip(0, 7)
        #Constrain to stay within the screen
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

    def set_position(self, coordx, coordy):
        self.rect.top = coordy
        self.rect.left = coordx
    
class Player2(pygame.sprite.Sprite):

    def __init__(self):
        super(Player2, self).__init__()
        self.surf = pygame.Surface((15, 100))
        self.surf.fill((255, 120, 0))
        self.rect = self.surf.get_rect()

    # Move the sprite based on user keypresses
    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -7)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 7)
        #Constrain to stay within the screen
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

    def set_position(self, coordx, coordy):
        self.rect.top = coordy
        self.rect.left = coordx


class Ball(pygame.sprite.Sprite):
    
    def __init__(self):
        super(Ball, self).__init__()
        self.surf = (pygame.Surface((10, 10)))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect(
            center = (
                (SCREEN_WIDTH - self.surf.get_width()) / 2,
                (SCREEN_HEIGHT - self.surf.get_height()) / 2
            )
        )
        self.x_velocity = (distanceToNextPaddle * subdivision) / (120 * (120 / beatsPerMinute))
        self.run = True
        self.last_hit = ""
        self.last_vertical_hit = ""

        #This, rather than proportion of vertical movement, now represents the y velocity that is independent from x velocity
        self.y_velocity = (random.random() / 5) * 30 - 0.3
        #For the purposes of 'music pong' the absolute value of the x-velocity component of the ball will have to remain constant
        #in order to do any alignment of the ball bounces with a beat or subdivision

    
    def update(self):

        self.rect.move_ip(self.x_velocity, self.y_velocity)
        
        if (self.rect.right < 0): # If the ball exits the left side of the screen, a point is scored and the ball is reset
            scoreText.updateScore(1)
            player1.set_position(10, (SCREEN_HEIGHT - player1.surf.get_height()) / 2)
            player2.set_position(SCREEN_WIDTH - (player2.surf.get_width()) - 10 , (SCREEN_HEIGHT - player2.surf.get_height()) / 2)

            pygame.time.delay(1000)
            self.rect = self.surf.get_rect(
                center = (
                    (SCREEN_WIDTH - self.surf.get_width()) / 2,
                    (SCREEN_HEIGHT - self.surf.get_height()) / 2
                )
            )
            self.last_hit = ""
            self.x_velocity = (((SCREEN_WIDTH - 25) - (ball.rect.x + ball.surf.get_width())) * subdivision) / (120 * (120 / beatsPerMinute))
            self.y_velocity = (random.random()) * 4 - 2

        elif (self.rect.left > SCREEN_WIDTH): # If the ball exits the right side of the screen, a point is scored and the ball is reset
            scoreText.updateScore(0)
            player1.set_position(10, (SCREEN_HEIGHT - player1.surf.get_height()) / 2)
            player2.set_position(SCREEN_WIDTH - (player2.surf.get_width()) - 10 , (SCREEN_HEIGHT - player2.surf.get_height()) / 2)

            pygame.time.delay(1000)
            self.rect = self.surf.get_rect(
                center = (
                    (SCREEN_WIDTH - self.surf.get_width()) / 2,
                    (SCREEN_HEIGHT - self.surf.get_height()) / 2
                )
            )
            self.last_hit = ""
            self.x_velocity = (((SCREEN_WIDTH - 25) - (ball.rect.x + ball.surf.get_width())) * subdivision) / (120 * (120 / beatsPerMinute)) * -1
            self.y_velocity = (random.random()) * 6 - 3
    
        #If the ball hits the top or bottom, flip the y velocity modifier and play a sound
        if ((self.rect.top <= (self.surf.get_height() / 2)) & (self.last_vertical_hit != "top")):
            self.y_velocity = self.y_velocity * -1
            collision_sound.play()
            self.last_vertical_hit = "top"
        if ((self.rect.top >= (SCREEN_HEIGHT - self.surf.get_height() / 2)) & (self.last_vertical_hit != "bottom")):
            self.y_velocity = self.y_velocity * -1
            collision_sound.play()
            self.last_vertical_hit = "bottom"


    def flipVelocity(self, y_difference): #When the ball runs into a paddle

        if (y_difference != 0):
            y_flip = y_difference / abs(y_difference) * -1 # y_flip will be -1 or 1 to represent the direction up/down that the ball is moving after the collision
        else: # since we can't divide by 0, if the ball lands in the exact center of the paddle (y_difference == 0), set y_difference to random float between 0.05 and -0.05
            y_difference = random.random() - 0.5
            y_flip = y_difference / abs(y_difference)

        self.y_velocity = y_flip * (abs(y_difference) * 10 + 1) # y_velocity changes based on y_difference

        self.changeVelocity(self.x_velocity / abs(self.x_velocity) * -1) # x_velocity changes based on subdivision and distance to next paddle
        print("Velocity: " + str(self.x_velocity) + ", " + str(self.y_velocity))
        collision_sound.play()

    def changeVelocity(self, direction): # Change the x velocity of the ball depending on the new subdivision      
        print("Distance to next paddle: " + str(distanceToNextPaddle))       
        self.x_velocity = (distanceToNextPaddle * subdivision) / (120 * (120 / beatsPerMinute)) * direction

class Text(pygame.sprite.Sprite):

    def __init__(self):
        super(Text, self).__init__()
        self.text = pygame.font.SysFont("Comic Sans MS", 30)
        self.score_left = 0
        self.score_right = 0
        self.surf = self.text.render("" + str(self.score_left) + " : " + str(self.score_right), False, (150, 255, 255))
        self.pos = ((SCREEN_WIDTH - self.surf.get_width()) / 2, (SCREEN_HEIGHT - self.surf.get_height()) / 2)

    def updateScore(self, player):
        if player == 0:
            self.score_left = self.score_left + 1
        if player == 1:
            self.score_right = self.score_right + 1
        self.surf = self.text.render("" + str(self.score_left) + " : " + str(self.score_right), False, (150, 255, 255))
        self.pos = ((SCREEN_WIDTH - self.surf.get_width()) / 2, (SCREEN_HEIGHT - self.surf.get_height()) / 2)
        #Add logic to handle if the score reaches the win threshold



#Initialize sounds (to change defaults, call before pygame.init)
pygame.mixer.init()

#Initialize pygame
pygame.init()


#Add and load sounds
collision_sound = pygame.mixer.Sound("bonk-sound-effect-1.mp3")

#Create the actual display surface using display.set_mode that is the size of the fullscreen
fullscreen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

#Create screen object of size SCREEN_WIDTH x SCREEN_HEIGHT
screen = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))




#Instantiate player 1 rectangle
player1 = Player1()
player1.set_position(10, (SCREEN_HEIGHT - player1.surf.get_height()) / 2)

#Instantiate player 2 rectangle
player2 = Player2()
player2.set_position(SCREEN_WIDTH - (player2.surf.get_width()) - 10 , (SCREEN_HEIGHT - player2.surf.get_height()) / 2)

#Instantiate ball
ball = Ball()
distanceToNextPaddle = (SCREEN_WIDTH - 25) - (ball.rect.x + ball.surf.get_width()) # Difference between left edge of right paddle and right edge of ball

#Instantiate text
scoreText = Text()

# Create groups to hold ball sprite and all sprites
# players is used for rendering
players = pygame.sprite.Group()
players.add(player1)
players.add(player2)



#Setup a clock for setting a fixed frame rate
clock = pygame.time.Clock()


#MAIN LOOP
while ball.run:
    #Look at each event in the queue
    for event in pygame.event.get():
        #Is the event a key press?
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                print("Quitting from escape")
                ball.run = False
        
        #Is the event the window close button?
        elif event.type == QUIT:
            print("Quitting from close button")
            ball.run = False

    #Get the set of keys pressed and check for user input
    pressed_keys = pygame.key.get_pressed()

    #Update the player sprite based on user keypresses
    player1.update(pressed_keys)
    player2.update(pressed_keys)
    #Update the ball
    ball.update()

    #Reset screen to black before adding the objects to each frame
    screen.fill((0,0,0))
    #Draw all sprites
    for entity in players:
        screen.blit(entity.surf, entity.rect)
    screen.blit(ball.surf, ball.rect)
    screen.blit(scoreText.surf, scoreText.pos)

    #Scale screen to the fullscreen size (this is in the game loop)
    scaled = pygame.transform.smoothscale(screen, fullscreen.get_size())
    fullscreen.blit(scaled, (0, 0))

    #Update visual frame
    pygame.display.flip()

    #Ensure program maintains a rate of 60 fps
    clock.tick(60)

    #Check if the ball has collided with either player
    if (pygame.sprite.collide_rect(ball, player1) & (ball.last_hit != "left")):
        distanceToNextPaddle = (SCREEN_WIDTH - 25) - (ball.rect.x + ball.surf.get_width())
        ball.flipVelocity((player1.rect.y + (player1.surf.get_height() / 2)  - (ball.rect.y + (ball.surf.get_height() / 2))) / player1.surf.get_height())
        
        ball.last_hit = "left"
        ball.last_vertical_hit = ""
    if (pygame.sprite.collide_rect(ball, player2) & (ball.last_hit != "right")):
        distanceToNextPaddle = ball.rect.x - 25
        ball.flipVelocity((player2.rect.y + (player2.surf.get_height() / 2)  - (ball.rect.y + (ball.surf.get_height() / 2))) / player2.surf.get_height())
        
        ball.last_hit = "right"
        ball.last_vertical_hit = ""


print("Game loop exit")
pygame.mixer.music.stop()
pygame.mixer.quit()
pygame.quit()