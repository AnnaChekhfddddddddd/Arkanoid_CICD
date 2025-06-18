import pygame
import argparse

# Налаштування
parser = argparse.ArgumentParser(description="Arkanoid Game")
parser.add_argument('--difficulty', choices=['easy', 'medium', 'hard'], default='medium')
parser.add_argument('--bg-color', type=str, default='pink')
args = parser.parse_args()

DIFFICULTY = {
    'easy': {'ball_speed': 4, 'paddle_width': 150},
    'medium': {'ball_speed': 5, 'paddle_width': 100},
    'hard': {'ball_speed': 6, 'paddle_width': 50}
}

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Arkanoid")
COLORS = {
    'black': (0, 0, 0),
    'pink': (255, 105, 180),
    'white': (255, 255, 255),
    'blue': (0, 0, 255),
    'red': (255, 0, 0)
}
BG_COLOR = COLORS.get(args.bg_color, COLORS['pink'])

# Paddle
class Paddle:
    def __init__(self):
        self.width = DIFFICULTY[args.difficulty]['paddle_width']
        self.height = 20
        self.x = (WIDTH - self.width) // 2
        self.y = HEIGHT - 40
        self.speed = 10

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.x > 0:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] and self.x < WIDTH - self.width:
            self.x += self.speed

    def draw(self, screen):
        pygame.draw.rect(screen, COLORS['white'], (self.x, self.y, self.width, self.height))

# Ball
class Ball:
    def __init__(self):
        self.radius = 10
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.dx = DIFFICULTY[args.difficulty]['ball_speed']
        self.dy = -DIFFICULTY[args.difficulty]['ball_speed']

    def move(self):
        self.x += self.dx
        self.y += self.dy
        if self.x <= self.radius or self.x >= WIDTH - self.radius:
            self.dx = -self.dx
        if self.y <= self.radius:
            self.dy = -self.dy

    def collide_with_paddle(self, paddle):
        if (self.y + self.radius >= paddle.y and
            paddle.x <= self.x <= paddle.x + paddle.width):
            self.dy = -self.dy

    def draw(self, screen):
        pygame.draw.circle(screen, COLORS['white'], (int(self.x), int(self.y)), self.radius)

# Brick
class Brick:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 80
        self.height = 30
        self.is_destroyed = False

    def draw(self, screen):
        if not self.is_destroyed:
            pygame.draw.rect(screen, COLORS['white'], (self.x, self.y, self.width, self.height))

    def destroy(self):
        self.is_destroyed = True

# Config
class Config:
    def __init__(self):
        self.difficulty = args.difficulty
        self.bg_color = args.bg_color

    def parse_args(self):
        return self.difficulty, self.bg_color

# Game
class Game:
    def __init__(self, config):
        self.paddle = Paddle()
        self.ball = Ball()
        self.bricks = [Brick(x, y) for y in range(50, 200, 40) for x in range(50, WIDTH - 50, 90)]
        self.score = 0
        self.lives = 3
        self.running = True

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update(self):
        self.paddle.move()
        self.ball.move()
        self.ball.collide_with_paddle(self.paddle)
        for brick in self.bricks:
            if not brick.is_destroyed:
                if (self.ball.y - self.ball.radius <= brick.y + brick.height and
                    self.ball.y + self.ball.radius >= brick.y and
                    brick.x <= self.ball.x <= brick.x + brick.width):
                    brick.destroy()
                    self.ball.dy = -self.ball.dy
                    self.score += 10
        if self.ball.y > HEIGHT:
            self.lives -= 1
            self.ball = Ball()
            if self.lives == 0:
                self.game_over()
        if all(brick.is_destroyed for brick in self.bricks):  # Перевірка перемоги
            self.game_over()

    def render(self):
        screen.fill(BG_COLOR)
        self.paddle.draw(screen)
        self.ball.draw(screen)
        for brick in self.bricks:
            brick.draw(screen)
        font = pygame.font.SysFont(None, 36)
        score_text = font.render(f"Score: {self.score}", True, COLORS['white'])
        lives_text = font.render(f"Lives: {self.lives}", True, COLORS['white'])
        screen.blit(score_text, (10, 10))
        screen.blit(lives_text, (WIDTH - 100, 10))
        pygame.display.flip()

    def game_over(self):
        font = pygame.font.SysFont(None, 48)
        if self.lives == 0:
            game_over_text = font.render("Game Over! Play again? (Y/N)", True, COLORS['red'])
        else:  # Перемога
            game_over_text = font.render("You Win! Play again? (Y/N)", True, COLORS['red'])
        screen.blit(game_over_text, (WIDTH // 2 - 150, HEIGHT // 2))
        pygame.display.flip()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_y:
                        self.reset_game()
                        return
                    elif event.key == pygame.K_n:
                        self.running = False
                        return

    def reset_game(self):
        self.paddle = Paddle()
        self.ball = Ball()
        self.bricks = [Brick(x, y) for y in range(50, 200, 40) for x in range(50, WIDTH - 50, 90)]
        self.score = 0
        self.lives = 3

    def run(self):
        clock = pygame.time.Clock()
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            clock.tick(60)

if __name__ == "__main__":
    config = Config()
    game = Game(config)
    game.run()
    pygame.quit()