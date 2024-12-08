import pygame

from pong_common import GameState, Ball, Paddle, SCREEN_HEIGHT, SCREEN_WIDTH, SCORE

FONT = pygame.font.get_default_font()

class howToScreen():
    def __init__(self, score, color):
        self.how_to_text_one = score.render(
            f"Buy flowers/walnuts using a key combo", False, color
        )
        self.how_to_text_two = score.render(
            f"For flowers use F and numbers 1-9 for placement", False, color
        )
        self.how_to_text_three = score.render(
            f"For walnuts use R and numbers 1-9 for placement", False, color
        )
        self.how_to_text_four = score.render(
            f"Gain sun points every time ball passes through flower", False, color
        )
        self.how_to_text_five = score.render(
            f"Defend incoming balls with walnuts", False, color
        )
    def draw(self, settings):
        settings.screen.blit(
            self.how_to_text_one, ((SCREEN_WIDTH // 2) - self.how_to_text_one.get_width() // 2, (SCREEN_HEIGHT // 2) - 200 )
        )
        settings.screen.blit(
            self.how_to_text_two, ((SCREEN_WIDTH // 2) - self.how_to_text_two.get_width() // 2, (SCREEN_HEIGHT // 2) - 100)
        )
        settings.screen.blit(
            self.how_to_text_three, ((SCREEN_WIDTH // 2) - self.how_to_text_three.get_width() // 2, SCREEN_HEIGHT // 2)
        )
        settings.screen.blit(
            self.how_to_text_four, ((SCREEN_WIDTH // 2) - self.how_to_text_four.get_width() // 2, (SCREEN_HEIGHT // 2) + 100)
        )
        settings.screen.blit(
            self.how_to_text_five, ((SCREEN_WIDTH // 2) - self.how_to_text_five.get_width() // 2, (SCREEN_HEIGHT // 2) + 200)
        )

class Shop():
    def __init__(self):
        self.walnut_cost = 60
        self.flower_cost = 20
        self.font = pygame.font.Font(pygame.font.get_default_font(), 20)
        self.player_score = 20;
        self.grid = ["n", "n", "n", "n", "n", "n", "n", "n", "n"]
        self.loc_help_x = [190, 315, 442, 190, 315, 442, 190, 315, 442]
        self.loc_help_y = [420, 420, 420, 300, 300, 300, 180, 180, 180]

    def draw(self, screen):
        shop_text = self.font.render(
            f"Flower: {self.flower_cost} points | Walnut: {self.walnut_cost} points |"
        )
        screen.blit(shop_text, self.position)

    def buy_walnut(self, location, list):
        if self.player_score >= 60:
            if self.grid[location] == "n":
                self.player_score -= 60
                self.grid[location] = "r"
                walnut = Walnut(self.loc_help_x[location], self.loc_help_y[location], (210, 125, 45), self, location)
                list.add(walnut)


    def buy_flower(self, location, list):
        if self.player_score >= 20:
            if self.grid[location] == "n":
                self.player_score -= 20
                self.grid[location] = "f"
                flower = Flower(self.loc_help_x[location], self.loc_help_y[location], (246, 214, 214), self)
                list.add(flower)

class Walnut(pygame.sprite.Sprite):
    def __init__(self, x, y, color, shop, loc):
        super().__init__()
        self.surf = pygame.Surface((SCREEN_WIDTH / 10, (SCREEN_HEIGHT / 5) - 2))
        self.surf.fill(color)
        self.rect = self.surf.get_rect(center=(x, y))
        self.center = self.rect.center
        self.health = 3
        self.current_color = (210, 125, 45)
        self.loc = loc
        self.shop = shop
        self.touched = False

    def update(self):
        if self.health == 2:
            self.current_color = (254, 255, 159)  
        elif self.health == 1:
            self.current_color = (211, 1, 28)  
        elif self.health == 0:
            self.kill()  
            self.shop.grid[self.loc] = "n"
        self.surf.fill(self.current_color)

    
    def collide_ball(self, ball):
        if self.rect.colliderect(ball.rect) and not self.touched:
            ball.x_vel *= -1
            ball.y_vel *= -1
            if ball.rect.centerx < self.rect.left:
                ball.rect.right = self.rect.left 
            elif ball.rect.centerx > self.rect.right:
                ball.rect.left = self.rect.right 

            if ball.rect.centery < self.rect.top:
                ball.rect.bottom = self.rect.top 
            elif ball.rect.centery > self.rect.bottom:
                ball.rect.top = self.rect.bottom 
            self.health -= 1  
            self.update()  
            self.touched = True            
    
    def reset(self):
        pass

class Flower(pygame.sprite.Sprite):
    def __init__(self, x, y, color, shop):
        super().__init__()
        self.surf = pygame.Surface((SCREEN_WIDTH / 12, SCREEN_HEIGHT / 8))
        self.surf.fill(color)
        self.rect = self.surf.get_rect(center=(x, y)) 
        self.blink = 100
        self.color = color
        self.shop = shop
        self.touched = False
        self.opp_color = (254, 255, 159)

    def update(self):
        if self.touched and self.blink > 0:
            if self.blink % 10 == 0 or self.blink % 9 == 0 or self.blink % 8 == 0:
                self.surf.fill(self.color)
            else:
                self.surf.fill(self.opp_color) 
            self.blink -= 1 
        elif self.blink == 0:
            self.surf.fill(self.color)
            self.touched = False

    def collide_ball(self, ball):
        if self.rect.colliderect(ball.rect):
            self.surf.fill(self.opp_color)
            if self.touched == False:
                self.blink = 99
                self.shop.player_score += 20
                self.touched = True
            #points increase for player
    
    def reset(self):
        pass
        

def run(settings):
    running = True
    state = GameState()

    light_green = (144, 238, 144)
    dark_green = (114, 191, 120)
    light_yellow = (254, 255, 159)
    light_pink = (246, 214, 214)
    light_blue = (128, 196, 233)
    darker_blue = (67, 53, 167)
    square_height = SCREEN_HEIGHT // 5
    square_width = SCREEN_WIDTH // 8

    ball = Ball((255, 255, 255), None)
    player = Paddle(SCREEN_WIDTH / 10, SCREEN_HEIGHT / 2, settings.p1_controls)
    player2 = Paddle((SCREEN_WIDTH * 9) / 10, SCREEN_HEIGHT / 2, settings.p2_controls)
    score = pygame.font.Font(FONT, 30)
    score_text = score.render(
        f"{state.p1score} - {state.p2score}", False, (255, 255, 255)
    )
    howTo = howToScreen(score, darker_blue)
    store = Shop()


    sun_two = score.render(
        f"Sun Points : 20", False, light_pink
    )

    flower_shop = score.render(
        f"Flower Cost: 20 points", False, darker_blue
    )
    walnut_shop = score.render(
        f"Walnut Cost: 60 points", False, darker_blue
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
    how_to_timer = 0.0;

    while running:
        settings.screen.fill((0, 0, 0))

        for row in range(0, SCREEN_HEIGHT, square_height):
            for col in range(0, SCREEN_WIDTH, square_width):
                color = light_green if (row // square_height + col // square_width) % 2 == 0 else dark_green
                pygame.draw.rect(settings.screen, color, pygame.Rect(col, row, square_width, square_height))
        
        pygame.draw.rect(settings.screen, (255, 255, 255), pygame.Rect(SCREEN_WIDTH // 2, 0, 5, SCREEN_HEIGHT))


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

        if how_to_timer < 3:
            for entity in all_sprites:
                settings.screen.blit(entity.surf, entity.rect)

            howTo.draw(settings)
            how_to_timer += dt
            pygame.display.flip()
            dt = clock.tick(120) / 1000.0
            continue

        ball.update(dt, state)
        ball.collide(paddles, dt)
        keys = pygame.key.get_pressed()

        for paddle in paddles:
            paddle.update(keys, ball.rect.centery, ball.rect.centerx, dt)

        for walnut in all_sprites:
            if isinstance(walnut, Walnut):
                walnut.touched = False

        for entity in all_sprites:
            if isinstance(entity, Flower): 
                entity.update()
            if isinstance(entity, Walnut):
                entity.update()
            settings.screen.blit(entity.surf, entity.rect)

        for flower in all_sprites:
            if isinstance(flower, Flower):
                flower.collide_ball(ball)
            if isinstance(flower, Walnut):
                flower.collide_ball(ball)

        if keys[pygame.K_f]:
            count = 0
            for loc in range(pygame.K_1, pygame.K_9 + 1):
                if keys[loc]:
                    store.buy_flower(count, all_sprites)
                count += 1

        if keys[pygame.K_r]:
            count = 0
            for loc in range(pygame.K_1, pygame.K_9 + 1):
                if keys[loc]:
                    store.buy_walnut(count, all_sprites)
                count += 1

        sun_one = score.render(
            f"Sun Points : {store.player_score}", False, light_yellow
        )

        settings.screen.blit(
            score_text, ((int(SCREEN_WIDTH // 2.11), (SCREEN_HEIGHT * 9) / 10))
        )
        settings.screen.blit(
            sun_one, ((20), ((SCREEN_HEIGHT * 9) / 10))
        )
        settings.screen.blit(
            sun_two, ((SCREEN_WIDTH - 270), ((SCREEN_HEIGHT * 9) / 10))
        )

        settings.screen.blit(
            flower_shop, ((20), (20))
        )
        settings.screen.blit(
            walnut_shop, ((SCREEN_WIDTH - 480), (20))
        )

        pygame.display.flip()
        dt = clock.tick(120) / 1000.0
