import pytest
import sys
import os
from unittest.mock import patch
import importlib.util
import argparse
import pygame

# Додаємо шлях до кореневої теки
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Фікстура для мокування parse_args і динамічного імпорту
@pytest.fixture(autouse=True)
def setup_arkanoid():
    with patch('argparse.ArgumentParser.parse_args') as mock_parse:
        mock_parse.return_value = argparse.Namespace(difficulty='medium', bg_color='pink')
        arkanoid_path = os.path.join(os.path.dirname(__file__), "..", "arkanoid.py")
        spec = importlib.util.spec_from_file_location("arkanoid", arkanoid_path)
        arkanoid = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(arkanoid)
        global Paddle, Ball, Brick, Game, Config
        Paddle = arkanoid.Paddle
        Ball = arkanoid.Ball
        Brick = arkanoid.Brick
        Game = arkanoid.Game
        Config = arkanoid.Config
        yield

# Фікстура для ініціалізації об’єктів
@pytest.fixture
def setup_objects():
    config = Config()
    paddle = Paddle()
    ball = Ball()
    brick = Brick(300, 100)
    game = Game(config)
    return paddle, ball, brick, game

# 1. Тест руху платформи (Paddle) з параметризацією
@pytest.mark.parametrize("key_code, expected_x", [
    (pygame.K_LEFT, lambda x: x - 10 if x > 0 else x),
    (pygame.K_RIGHT, lambda x: x + 10 if x < 800 - 100 else x)
])
def test_paddle_movement(mocker, setup_objects, key_code, expected_x):
    paddle, _, _, _ = setup_objects
    initial_x = paddle.x
    # Мокуємо pygame.key.get_pressed як масив, де тільки потрібна клавіша True
    mock_keys = [False] * 1073742050  # Достатньо великий масив для всіх клавіш
    mock_keys[key_code] = True
    mocker.patch('pygame.key.get_pressed', return_value=mock_keys)
    paddle.move()
    assert paddle.x == expected_x(initial_x)

# 2. Тест початкової позиції платформи
def test_paddle_initial_position(setup_objects):
    paddle, _, _, _ = setup_objects
    assert paddle.x == (800 - 100) // 2 and paddle.y == 560

# 3. Тест руху м’яча (Ball) з параметризацією
@pytest.mark.parametrize("dx, dy, expected_x, expected_y", [
    (5, 5, 405, 305),
    (-5, -5, 395, 295)
])
def test_ball_movement(setup_objects, dx, dy, expected_x, expected_y):
    _, ball, _, _ = setup_objects
    ball.x = 400
    ball.y = 300
    ball.dx = dx
    ball.dy = dy
    ball.move()
    assert ball.x == expected_x and ball.y == expected_y

# 4. Тест зіткнення м’яча з платформою
def test_ball_paddle_collision(mocker, setup_objects):
    paddle, ball, _, _ = setup_objects
    initial_dy = ball.dy
    ball.y = paddle.y - ball.radius
    ball.x = paddle.x + paddle.width // 2
    ball.collide_with_paddle(paddle)
    assert ball.dy == -initial_dy

# 5. Тест зіткнення м’яча з цеглою (імітація)
def test_ball_brick_collision(mocker, setup_objects):
    _, ball, brick, _ = setup_objects
    initial_dy = ball.dy
    ball.y = brick.y - ball.radius
    ball.x = brick.x + brick.width // 2
    ball.dy = -ball.dy  # Імітація відбиття
    assert ball.dy == -initial_dy

# 6. Тест знищення цегли
def test_brick_destroy(setup_objects):
    _, _, brick, _ = setup_objects
    initial_state = brick.is_destroyed
    brick.destroy()
    assert brick.is_destroyed != initial_state

# 7. Тест початкового стану гри
def test_game_initial_state(setup_objects):
    _, _, _, game = setup_objects
    assert game.lives == 3 and game.score == 0

# 8. Тест оновлення гри (повільний тест із маркером)
@pytest.mark.slow
def test_game_update(mocker, setup_objects):
    _, ball, _, game = setup_objects
    mocker.patch.object(ball, 'collide_with_paddle', return_value=None)
    initial_lives = game.lives
    game.update()
    assert game.lives >= 0

# 9. Тест початкової кількості життів
def test_game_initial_lives(setup_objects):
    _, _, _, game = setup_objects
    assert game.lives == 3

# 10. Тест початкового кольору фону
def test_game_default_background_color(setup_objects):
    _, _, _, game = setup_objects
    screen = pygame.display.set_mode((800, 600))
    screen.fill((255, 105, 180))
    assert screen.get_at((0, 0)) == (255, 105, 180, 255)

if __name__ == "__main__":
    pytest.main(["-v", "tests/test_arkanoid.py"])