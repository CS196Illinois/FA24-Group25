#Import pygame module
import pygame

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


#Define screen size
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600


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
            self.rect.move_ip(0, -5)
        if pressed_keys[K_s]:
            self.rect.move_ip(0, 5)
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
        self.surf.fill((255, 0, 0))
        self.rect = self.surf.get_rect()

    # Move the sprite based on user keypresses
    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
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
        super(Ball, self).__init__
        self.surf = (pygame.Surface((10, 10)))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect(
            center = (
                (SCREEN_WIDTH - self.surf.get_width()) / 2,
                (SCREEN_HEIGHT - self.surf.get_height()) / 2
            )
        )
        self.speed = 10
        self.proportion_x = 0.5
        self.proportion_y = -0.5
        self.game_running = True #FIXME this doesn't work right now
    
    def update(self):

        self.rect.move_ip(self.speed * self.proportion_x, self.speed * self.proportion_y)
        if (self.rect.right < 0 | self.rect.left > SCREEN_WIDTH):
            self.game_running = False
            self.kill()
    
        if (self.rect.top <= (self.surf.get_height() / 2)):
            self.proportion_y = self.proportion_y * -1
            collision_sound.play()
        if (self.rect.top >= (SCREEN_HEIGHT - self.surf.get_height() / 2)):
            self.proportion_y = self.proportion_y * -1
            collision_sound.play()


    def flipVelocity(self):
        self.proportion_x = self.proportion_x * -1
        collision_sound.play()

#Initialize sounds (to change defaults, call before pygame.init)
pygame.mixer.init()

#Initialize pygame
pygame.init()


#Add and load sounds
collision_sound = pygame.mixer.Sound("bonk-sound-effect.FLAC")

#Create screen object of size SCREEN_WIDTH x SCREEN_HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

#Instantiate player 1 rectangle
player1 = Player1()
player1.set_position(10, (SCREEN_HEIGHT - player1.surf.get_height()) / 2)

#Instantiate player 2 rectangle
player2 = Player2()
player2.set_position(SCREEN_WIDTH - (player2.surf.get_width()) - 10 , (SCREEN_HEIGHT - player2.surf.get_height()) / 2)

#Instantiate ball
ball = Ball()

# Create groups to hold ball sprite and all sprites
# - players is used for collision detection
# - all_sprites is used for rendering
players = pygame.sprite.Group()
players.add(player1)
players.add(player2)


#Variable to keep the main loop running
running = True

#Setup a clock for decent frame rate
clock = pygame.time.Clock()

#MAIN LOOP
while ball.game_running:
    #Look at each event in the queue
    for event in pygame.event.get():
        #Is the event a key press?
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                ball.game_running = False
        
        #Is the event the window close button?
        elif event.type == QUIT:
            ball.game_running = False

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
    #Update visual frame
    pygame.display.flip()

    #Ensure program maintains a rate of 30 fps
    clock.tick(60)

    #Check if the ball has collided with either player
    if pygame.sprite.spritecollideany(ball, players):
        ball.flipVelocity()

pygame.mixer.music.stop()
pygame.mixer.quit
