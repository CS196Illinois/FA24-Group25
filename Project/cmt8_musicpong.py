import pygame
import math
import random

from pong_common import GameState, Paddle, SCREEN_HEIGHT, SCREEN_WIDTH, SCORE

FONT = pygame.font.get_default_font()
collision_sound = pygame.mixer.Sound("bonk-sound-effect-1.mp3")

# copied from Mariano's edition of the ball class but with edits to be useful for music pong
class MusicBall(pygame.sprite.Sprite):
    # Todo: update ball constructor to take size (and consider other useful additions)
    def __init__(self, bpm, subdivision):
        super(MusicBall, self).__init__()

        self.surf = pygame.Surface((15, 15))

        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))

        self.speed = 500.0 # this version of pong should not have a variable for the speed because the x velocity component will have to be changed directly
        # the y component of the velocity will operate wihtout regard to the x component

        self.bpm = bpm
        self.subdivision = subdivision
        print("Creating MusicBall where BPM = " + str(bpm) + " and subdivision = " + str(subdivision))

        self.angle = math.pi + random.randint(0, 1) * math.pi

        self.x_vel = self.speed * math.cos(self.angle) 
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

        # get rid 
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
                self.rect.move_ip(self.x_vel * dt, -self.y_vel * dt)

                
                distanceToNextPaddle = paddles.sprites().__getitem__(1).rect.left - self.rect.right
                if (movingRightBeforeCollision):
                    distanceToNextPaddle = paddles.sprites().__getitem__(0).rect.right - self.rect.left
                print("distance to next paddle: " + str(distanceToNextPaddle))


                # formula for how many pixels the ball has to move per millisecond in order to line up the next hit on the required musical subdivision
                self.x_vel = distanceToNextPaddle * self.bpm * self.subdivision / 240
                print(str(self.x_vel))
                

                #phi = 0.3 * math.pi * (2 * offset - 1)
                
                phi = 0.4 * math.pi * (2 * offset - 1)
                self.y_vel = self.speed * math.sin(phi * 1.2)
                print(str(self.y_vel))
                self.angle = math.atan2(self.y_vel, self.x_vel)
                collision_sound.play()

    # figured this might be useful boilerplate
    def set_speed(self, speed: int):
        pass

    def reset(self):
        self.speed = 500
        self.angle = math.pi + random.randint(0, 1) * math.pi
        self.rect.centerx = int(SCREEN_WIDTH / 2)
        self.rect.centery = int(SCREEN_HEIGHT / 2)


def run(settings):
    running = True
    state = GameState()
    

    # Specific to music pong
    beatsPerMinute = 60
    subdivision = 2 # 1: whole note subdivision, 2: half note subdivision, 4: quarter note subdivision and so on


    ball = MusicBall(beatsPerMinute, subdivision)
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
                running = False

            if event.type == SCORE:
                score_text = score.render(
                    f"{state.p1score} - {state.p2score}", False, (255, 255, 255)
                )
                for entity in all_sprites:
                    entity.reset()

        if state.p2score > 5 or state.p1score > 5:
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
