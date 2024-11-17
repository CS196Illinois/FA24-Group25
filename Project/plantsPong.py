# Simple pygame program

# Import and initialize the pygame library
import pygame
import pygame.draw_py
import pygame.freetype
from pygame.constants import K_UP, K_DOWN, K_s, K_w
from pong_common import GameState, Ball, Paddle, SCREEN_HEIGHT, SCREEN_WIDTH, SCORE

#pygame.init()

#colors
BLUE = (0,0,255)
BLACK = (0,0,0)
GREEN = (100, 200, 100)
YELLOW = (255, 191, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
PINK = (255, 192, 203)

#ask how to put in pixel art stuff so that flowers and everything look like
# actual objects!!!

'''
class Obstacle(pygame.sprite.Sprite):
    def __init__(self, xLoc, yLoc, width, height):
        super().__init__()

        self.image = pygame.Surface((width, height))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect((xLoc, yLoc))


    divide the place into an array and put weight into different sections for where there is less objects
    extend mariano's classes and use his obstacle or whatever class in order to further inplement this class
    create a toPosition method which places obstacle in certain section of the screen
    create a toRandom method which selects a random space and then selects a random width and height for the class
    (maybe can have like tetris peices?)
'''

class Shop():
    def __init__(self, x, y):
        self.position = (x, y)
        self.walnut_cost = 45
        self.flower_cost = 5
        self.font = pygame.font.Font(pygame.font.get_default_font(), 20)

    def draw(self, screen):
        shop_text = self.font.render(
            f"Flower: {self.flower_cost} sun points | Walnut: {self.walnut_cost} sun points |"
        )
        screen.blit(shop_text, self.position)

    def buy_walnut(self, player_type, player_score):
        pass

    def buy_flower(self, player_type, player_score):
        pass

class Walnut(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((SCREEN_WIDTH / 10, SCREEN_HEIGHT / 5))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect(center=(x, y))
        self.health = 3

    def update(self):
        if self.health == 2:
            self.image.fill(YELLOW)
        if self.health == 1:
            self.image.fill(RED)
        if self.health == 0:
            self.kill()

    
    def collide_ball(self, ball):
        if self.rect.colliderect(ball.rect):
            ball.x_vel *= -1
            self.health -= 1

class Flower(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((SCREEN_WIDTH / 10, SCREEN_HEIGHT / 5))
        self.image.fill(PINK)
        self.rect = self.image.get_rect(center=(x, y)) 
        self.blink = 10
        #here convert the image

    def update(self):
        if self.blink < 10 & self.blink > 0:
            if self.blink % 2 == 0:
                self.image.fill(PINK)
            else:
                self.image.fill(BLUE)
        elif self.blink == 0:
            self.blink = 10
            self.image.fill(PINK)

    def collide_ball(self, ball):
        if self.rect.colliderect(ball.rect):
            self.image.fill(BLUE)
            self.blink -= 1
            #points increase for player

class PlantsGameState(GameState):
    def __init__(self):
        super().__init__()
        self.sunPointsPlayer1 = 15
        self.sunPointsPlayer2 = 15

def run(settings):
    running = True
    state = GameState()
    #plantState = PlantsGameState(state);

    ball = Ball((255,255,255))
    player1 = Paddle(SCREEN_WIDTH / 10, SCREEN_HEIGHT / 2, (K_w, K_s), size=60)
    player2 = Paddle(SCREEN_WIDTH / 10, SCREEN_HEIGHT / 2, (K_UP, K_DOWN), size=60)
    score = pygame.font.Font(pygame.font.get_default_font(), 20)
    score_text = score.render(
        f"{state.p1score} - {state.p2score}", False, (255,255,255)
    )

    clock = pygame.time.Clock()

    moving_objects = pygame.sprite.Group()
    moving_objects.add(ball)
    moving_objects.add(player1)
    moving_objects.add(player2)

    paddles = pygame.sprite.Group()
    paddles.add(player1)
    paddles.add(player2)

    #I need help with adding the walnuts because it will be based on if
    #the player buys a walnut with their points
    #also how do I ammend the paddle class to add points whenever the ball
    #is hit by the paddle 
    #or like make a flower class emi

    dt = 0

    while running:
        settings.screen.fill(BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == SCORE:
                score_text = score.render(
                    f"{state.p1score} - {state.p2score}", False, GREEN
                    #how do I add sun points to gamestate
                )
                for entity in moving_objects:
                    entity.reset()
        
        if state.p2score > 3 or state.p1score > 3:
            running = False
            state.reset()

        ball.update(dt)
        ball.collide(paddles, dt)
        keys = pygame.key.get_pressed()

        for paddle in paddles:
            paddle.update(keys, ball.rect.centery, ball.rect.centerx, dt)
        
        for entity in moving_objects:
            settings.screen.blit(entity.surf, entity.rect)
        
        settings.screen.blit(
            score_text, ((int(SCREEN_WIDTH / 2), (SCREEN_HEIGHT * 9) / 10))
        )
        #here do the flower image

        pygame.display.flip()
        dt = clock.tick(120) / 1000.0
