import pygame
import math
import random

from pong_common import GameState, Paddle, SCREEN_HEIGHT, SCREEN_WIDTH, SCORE

FONT = pygame.font.get_default_font()
collision_sound = pygame.mixer.Sound("bonk-sound-effect-1.wav")
tempo_warning_ping = pygame.mixer.Sound("tempoWarnPing.mp3")
chirp = pygame.mixer.Sound("chirp.mp3")

ticks = 0 # using to test real bpm of ball (somehow not matching ideal bpm)

# copied from Mariano's edition of the ball class but with edits to be useful for music pong
class MusicBall(pygame.sprite.Sprite):
    # Todo: update ball constructor to take size (and consider other useful additions)
    def __init__(self, bpm, subdivision):
        super(MusicBall, self).__init__()

        self.surf = pygame.Surface((15, 15))

        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))

        self.speed = 500.0

        self.bpm = bpm
        self.subdivision = subdivision
        print("Creating MusicBall where BPM = " + str(bpm) + " and subdivision = " + str(subdivision))

        self.angle = math.pi + random.randint(0, 1) * math.pi

        self.x_vel = 387 * self.bpm * self.subdivision / 240
        self.y_vel = self.speed * math.sin(self.angle)
        self.locked = False

    # dt is time since last frame
    def update(self, dt, state):
        self.rect.move_ip(self.x_vel * dt, self.y_vel * dt)
        if self.rect.left < 0:
            state.score(2)
        elif self.rect.right > SCREEN_WIDTH:
            state.score(1)
        if self.rect.top < 0:
            self.angle = math.atan2(-self.y_vel, self.x_vel)
            self.rect.top = 0
            collision_sound.play()
        if self.rect.bottom > SCREEN_HEIGHT:
            self.angle = math.atan2(-self.y_vel, self.x_vel)
            self.rect.bottom = SCREEN_HEIGHT
            collision_sound.play()

        # get rid of:
        # self.x_vel = math.cos(self.angle) * self.speed
        self.y_vel = math.sin(self.angle) * self.speed

    def collide(self, paddles, dt):
        for i in paddles:
            if i.rect.colliderect(self.rect):
                # ratio of difference in height between paddle center and ball center difference and sum
                offset = (self.rect.y + self.rect.height - i.rect.y) / (
                    i.rect.height + self.rect.height
                )

                movingRightBeforeCollision = self.x_vel > 0  # calculate distance to the next paddle that the ball must hit
                
                self.x_vel *= -1 #free the ball from recolliding

                #self.rect.move_ip(self.x_vel * dt, -self.y_vel * dt) #TODO teleport ball to edge of paddle and use exact calculable, nonvariable distance in calculations
                distanceToNextPaddle = 0
                if (movingRightBeforeCollision == False):
                    self.rect.x = paddles.sprites().__getitem__(0).rect.right #testing this
                    distanceToNextPaddle = paddles.sprites().__getitem__(1).rect.right - self.rect.right
                if (movingRightBeforeCollision):
                    self.rect.x = paddles.sprites().__getitem__(1).rect.left - self.rect.width #testing this
                    distanceToNextPaddle = paddles.sprites().__getitem__(0).rect.left - self.rect.left



                # formula for how many pixels the ball has to move per millisecond in order to line up the next hit on the required musical subdivision
                self.x_vel = distanceToNextPaddle * self.bpm * self.subdivision / 240
                
                
                phi = 0.4 * math.pi * (2 * offset - 1)
                
                
                self.y_vel = self.speed * math.sin(phi * 1.2)
                self.angle = math.atan2(self.y_vel, self.x_vel)
                self.rect.move_ip(self.x_vel * dt, self.y_vel * dt) #testing
                collision_sound.play()

    # figured this might be useful boilerplate
    def set_speed(self, speed: int):
        pass

    def reset(self):
        self.speed = 500
        self.angle = math.pi + random.randint(0, 1) * math.pi
        self.rect.centerx = int(SCREEN_WIDTH / 2)
        self.rect.centery = int(SCREEN_HEIGHT / 2)
        

class MusicControl:
    def __init__(self, bpm, subdivision, selected_song):
        self.bpm = bpm
        self.subdivision = subdivision
        self.selected_song = selected_song
        self.ball = MusicBall(self.bpm, self.subdivision)

    def queue_bpm_change(self, new):
        self.bpm = new
        timeToWait = 1000 #need to calculate based on bpm and subdivision. In milliseconds
        #introduce beeps before changing the active bpm
        tempo_warning_ping.play()
        pygame.time.set_timer(PLAYPING, timeToWait, 4)

        pygame.time.set_timer(CHANGEBPM, timeToWait * 4, 1)

    def queue_subdivision_change(self, new):
        self.subdivision = new
        timeToWait = 1000 #need to calculate based on bpm and subdivision. In milliseconds
        #introduce beeps before changing the active subdivision
        tempo_warning_ping.play()
        pygame.time.set_timer(PLAYPING, timeToWait, 4)

        pygame.time.set_timer(CHANGESUBDIVISION, timeToWait * 4, 1)

    def random_event(self):
        chirp.play()
        print("Random event occurring")
        pygame.time.set_timer(RECURRINGRANDOMEVENT, random.randint(10, 18) * 1000, 1) # sets timer to random time from 10 to 18 seconds

    
PLAYPING = pygame.USEREVENT + 10
CHANGEBPM = pygame.USEREVENT + 11
CHANGESUBDIVISION = pygame.USEREVENT + 12
RECURRINGRANDOMEVENT = pygame.USEREVENT + 13

def run(settings, selected_song):
    running = True
    state = GameState()

    pygame.mixer.music.load("machine120cut.wav") #TODO need to load specific song from selected_song parameter
    pygame.mixer.music.play(loops=-1)

    control = MusicControl(120, 2, selected_song)
    pygame.time.set_timer(RECURRINGRANDOMEVENT, random.randint(10, 18) * 1000, 1) # sets timer to random time from 10 to 18 seconds

    ball = control.ball
    player = Paddle(SCREEN_WIDTH / 10, SCREEN_HEIGHT / 2, settings.p1_controls)
    player2 = Paddle((SCREEN_WIDTH * 9) / 10, SCREEN_HEIGHT / 2, ())
    score = pygame.font.Font(FONT, 20)
    score_text = score.render(
        f"{state.p1score} - {state.p2score}", False, (255, 255, 255)
    )

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
        settings.screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mixer_music.stop()
                running = False

            if event.type == SCORE:
                score_text = score.render(
                    f"{state.p1score} - {state.p2score}", False, (255, 255, 255)
                )
                for entity in all_sprites:
                    entity.reset()
                control.bpm = 120
                control.subdivision = 2
                ball.bpm = control.bpm

            if event.type == pygame.MOUSEBUTTONDOWN:
                control.queue_subdivision_change(4)
            if event.type == PLAYPING:
                tempo_warning_ping.play()
            if event.type == CHANGEBPM:
                control.ball.bpm = control.bpm
            if event.type == CHANGESUBDIVISION:
                control.ball.subdivision = control.subdivision

            if event.type == RECURRINGRANDOMEVENT:
                control.random_event()

        if state.p2score > 5 or state.p1score > 5:
            pygame.mixer_music.stop()
            running = False

        ball.update(dt, state)
        ball.collide(paddles, dt)
        keys = pygame.key.get_pressed()

        for paddle in paddles:
            paddle.update(keys, ball.rect.centery, ball.rect.centerx, dt)

        for entity in all_sprites:
            settings.screen.blit(entity.surf, entity.rect)

        settings.screen.blit(
            score_text, ((int(SCREEN_WIDTH / 2), (SCREEN_HEIGHT * 9) / 10))
        )

        pygame.display.flip()
        dt = clock.tick(120) / 1000.0
