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