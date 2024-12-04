import pygame
import math
from pong_common import GameState, Ball, Paddle, SCREEN_HEIGHT, SCREEN_WIDTH, SCORE

FONT = pygame.font.get_default_font()
pygame.init()

# make npc paddle react time faster 
# make npc paddle slide 
# possibly: change bg to look like ice rink?


class Ball(Ball):
    def __init__(self, color, image):
        super().__init__(color, image)
        self.acceleration = -.005

    def collide(self, paddles, dt):
        self.speed = self.speed + (self.speed * self.acceleration) if self.speed > 500 else 500
        for i in paddles:
            if i.rect.colliderect(self.rect):
                offset = (self.rect.y + self.rect.height - i.rect.y) / (
                    i.rect.height + self.rect.height
                )
                self.x_vel *= -1
                self.rect.move_ip(self.x_vel * dt, -self.y_vel * dt)
                phi = 0.3 * math.pi * (2 * offset - 1)
                self.y_vel = self.speed * math.sin(phi)
                self.angle = math.atan2(self.y_vel, self.x_vel)
                self.speed = 900


class Paddle(Paddle):
    def __init__(self, x_pos, y_pos, controls, size=75, thresh=700):
        super().__init__(x_pos, y_pos, controls, size=75, thresh=700)
        self.acceleration = .01

    def update(self, pressed_keys, bally, ballx, dt):
        if len(self.controls) == 0 and ballx > self.thresh and ballx < self.rect.x:
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
                self.vel -= self.vel * self.acceleration

            if self.vel > self.max_vel:
                self.vel = self.max_vel
            elif self.vel < -self.max_vel:
                self.vel = -self.max_vel

        self.rect.move_ip(0, self.vel * dt)

        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
        elif self.rect.top < 0:
            self.rect.top = 0


def run(settings):
    running = True
    state = GameState()

    ball = Ball((255, 255, 255), None)
    player = Paddle(SCREEN_WIDTH / 10, SCREEN_HEIGHT / 2, settings.p1_controls)
    player2 = Paddle((SCREEN_WIDTH * 9) / 10, SCREEN_HEIGHT / 2, settings.p2_controls)
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