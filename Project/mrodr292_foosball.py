import pygame

from pong_common import GameState, Ball, Paddle, SCREEN_HEIGHT, SCREEN_WIDTH, SCORE

FONT = pygame.font.get_default_font()

pygame.init()


def run(settings):
    running = True
    state = GameState()
    state = GameState()

    ball = Ball((255, 255, 255), "Project/media/soccerball.png")
    player = Paddle(SCREEN_WIDTH / 10, SCREEN_HEIGHT / 2, settings.p1_controls, size=60)
    player2 = Paddle(
        (SCREEN_WIDTH * 4) / 10, SCREEN_HEIGHT / 2, settings.p2_controls, size=60
        (SCREEN_WIDTH * 4) / 10, SCREEN_HEIGHT / 2, settings.p2_controls, size=60
    )
    cpu1 = Paddle((SCREEN_WIDTH * 9) / 10, SCREEN_HEIGHT / 2, (), size=30, thresh=800)
    cpu2 = Paddle((SCREEN_WIDTH * 6) / 10, SCREEN_HEIGHT / 2, (), size=30, thresh=500)
    score = pygame.font.Font(FONT, 20)
    score_text = score.render(
        f"{state.p1score} - {state.p2score}", False, (255, 255, 255)
        f"{state.p1score} - {state.p2score}", False, (255, 255, 255)
    )

    clock = pygame.time.Clock()

    all_sprites = pygame.sprite.Group()
    all_sprites.add(ball)
    all_sprites.add(player)
    all_sprites.add(player2)
    all_sprites.add(cpu1)
    all_sprites.add(cpu2)

    paddles = pygame.sprite.Group()
    paddles.add(player)
    paddles.add(player2)
    paddles.add(cpu1)
    paddles.add(cpu2)

    dt = 0

    while running:
        settings.screen.fill((0, 128, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == SCORE:
                score_text = score.render(
                    f"{state.p1score} - {state.p2score}", False, (255, 255, 255)
                    f"{state.p1score} - {state.p2score}", False, (255, 255, 255)
                )
                for entity in all_sprites:
                    entity.reset()

        if state.p2score > 5 or state.p1score > 5:
        if state.p2score > 5 or state.p1score > 5:
            running = False

        ball.update(dt, state)
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
