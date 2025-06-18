import pygame
import argparse

# Налаштування
parser = argparse.ArgumentParser(description="Arkanoid Game")
parser.add_argument('--difficulty', choices=['easy', 'medium', 'hard'], default='medium')
parser.add_argument('--bg-color', type=str, default='black')
args = parser.parse_args()

DIFFICULTY = {
    'easy': {'ball_speed': 5, 'paddle_width': 150},
    'medium': {'ball_speed': 7, 'paddle_width': 100},
    'hard': {'ball_speed': 10, 'paddle_width': 50}
}

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Arkanoid")
COLORS = {'black': (0, 0, 0), 'blue': (0, 0, 255), 'white': (255, 255, 255)}
BG_COLOR = COLORS.get(args.bg_color, COLORS['black'])

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
# Game
class Game:
    def __init__(self):
        self.paddle = Paddle()
        self.ball = Ball()
        self.running = True

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update(self):
        self.paddle.move()
        self.ball.move()
        self.ball.collide_with_paddle(self.paddle)

    def render(self):
        screen.fill(BG_COLOR)
        self.paddle.draw(screen)
        self.ball.draw(screen)
        pygame.display.flip()

    def run(self):
        clock = pygame.time.Clock()
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            clock.tick(60)
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
            pygame.draw.rect(screen, COLORS['blue'], (self.x, self.y, self.width, self.height))

    def destroy(self):
        self.is_destroyed = True

if __name__ == "__main__":
    game = Game()
    game.run()
    pygame.quit()