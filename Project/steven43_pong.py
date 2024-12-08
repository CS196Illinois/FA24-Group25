import pygame
import math

from pygame.constants import K_a, K_d, K_LEFT, K_RIGHT
from pong_common import GameState, Ball, Paddle, SCREEN_HEIGHT, SCREEN_WIDTH, SCORE

FONT = pygame.font.get_default_font()

class AbilityBall(Ball):
    def __init__(self, color, image):
        super().__init__(color, image)
        self.lastHit = None
    
    def update(self, dt, state, pressed_keys):
        self.rect.move_ip(self.x_vel * dt, self.y_vel * dt)
        if self.rect.left < SCREEN_WIDTH * .02:
            state.score(2)
        elif self.rect.right > SCREEN_WIDTH * .98:
            state.score(1)
        if self.rect.top < 0 or self.rect.bottom > SCREEN_HEIGHT:
            self.y_vel *= -1
        self.surf.fill((255, 255, 255))
        if self.lastHit != None and len(self.lastHit.controls) > 1:
            if pressed_keys[self.lastHit.abilityControls[0]]:
                self.surf.fill((225, 225, 0))
                if self.lastHit.rect.centery > self.rect.centery:
                    self.y_vel = (self.y_vel * dt + .04) / dt
                if self.lastHit.rect.centery < self.rect.centery:
                    self.y_vel = (self.y_vel * dt - .04) / dt
        self.angle = math.atan2(self.y_vel, self.x_vel)

    def collide(self, paddles, dt):
        for i in paddles:
            if i.rect.colliderect(self.rect):
                self.lastHit = i
                self.surf.fill((225, 0, 255))
        super().collide(paddles, dt)

    def reset(self):
        super().reset()
        self.y_vel *= .5
        self.lastHit = None

class AbilityPaddle(Paddle):
    def __init__(self, x_pos, y_pos, controls, abilityControls, size=75, thresh=700):
        super().__init__(x_pos, y_pos, controls, size=75, thresh=700)
        self.abilityControls = abilityControls
        self.dashCooldownSeconds = 2
        self.timeSinceDash = self.dashCooldownSeconds
        self.dashSeconds = 10/120
        self.dashDirection = 1
        self.color = (255, 255, 255)

    def update(self, pressed_keys, bally, ballx, dt):
        self.timeSinceDash += 1/120
        if len(self.controls) == 0 and ballx > self.thresh and ballx < self.rect.x:
            if self.rect.top > bally:
                self.vel = -self.max_vel
            elif self.rect.bottom < bally:
                self.vel = self.max_vel
            else:
                self.vel = 0
        elif len(self.controls) > 1:
            if pressed_keys[self.abilityControls[1]] and self.timeSinceDash >= self.dashCooldownSeconds and (pressed_keys[self.controls[0]] or pressed_keys[self.controls[1]]):
                if pressed_keys[self.controls[0]]:
                    self.dashDirection = -1
                    self.timeSinceDash = 0
                elif pressed_keys[self.controls[1]]:
                    self.dashDirection = 1
                    self.timeSinceDash = 0
            elif pressed_keys[self.controls[0]]:
                self.vel -= self.max_vel
            elif pressed_keys[self.controls[1]]:
                self.vel += self.max_vel
            else:
                self.vel = 0

            if self.timeSinceDash <= self.dashSeconds:
                self.vel = 25000 / (self.dashSeconds * 120) * self.dashDirection
            else:
                if self.vel > self.max_vel:
                    self.vel = self.max_vel
                elif self.vel < -self.max_vel:
                    self.vel = -self.max_vel
            
            if self.timeSinceDash >= self.dashCooldownSeconds or self.timeSinceDash <= self.dashSeconds:
                if pressed_keys[self.abilityControls[0]]:
                    self.color = (255, 255, 0)
                else:
                    self.color = (255, 255, 255)
            else:
                if pressed_keys[self.abilityControls[0]]:
                    self.color = (128, 128, 0)
                else:
                    self.color = (128, 128, 128)
            self.surf.fill(self.color)
        
        self.rect.move_ip(0, self.vel * dt)

        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
        elif self.rect.top < 0:
            self.rect.top = 0

    def reset(self):
        super().reset()
        self.timeSinceDash = self.dashCooldownSeconds

def run(settings):
    running = True
    state = GameState()

    ball = AbilityBall((255, 255, 255), None)
    player = AbilityPaddle(SCREEN_WIDTH * .03, SCREEN_HEIGHT / 2, settings.p1_controls, (K_d, K_a))
    player2 = AbilityPaddle(SCREEN_WIDTH * .97, SCREEN_HEIGHT / 2, settings.p2_controls, (K_RIGHT, K_LEFT))
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

        keys = pygame.key.get_pressed()
        ball.update(dt, state, keys)
        ball.collide(paddles, dt)

        for paddle in paddles:
            paddle.update(keys, ball.rect.centery, ball.rect.centerx, dt)
            
        for entity in all_sprites:
            settings.screen.blit(entity.surf, entity.rect)

        settings.screen.blit(
            score_text, ((int(SCREEN_WIDTH / 2), (SCREEN_HEIGHT * 9) / 10))
        )

        pygame.display.flip()
        dt = clock.tick(120) / 1000.0