import random
import pygame as pg
from typing import Tuple


# Константы для размеров поля и сетки:
SCREEN_WIDTH: int = 640
SCREEN_HEIGHT: int = 480
GRID_SIZE: int = 20
GRID_WIDTH: int = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT: int = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP: Tuple[int, int] = (0, -1)
DOWN: Tuple[int, int] = (0, 1)
LEFT: Tuple[int, int] = (-1, 0)
RIGHT: Tuple[int, int] = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR: Tuple[int, int, int] = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR: Tuple[int, int, int] = (93, 216, 228)

# Цвет яблока
APPLE_COLOR: Tuple[int, int, int] = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR: Tuple[int, int, int] = (0, 255, 0)

# Скорость движения змейки:
SPEED: int = 20

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pg.display.set_caption(f'Змейка. Текущая скорость {SPEED}')
# Настройка времени:
clock = pg.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """Базовый класс для игровый объектов."""

    def __init__(self, body_color: Tuple[int, int, int] = APPLE_COLOR):
        """Инициализация GameObject"""
        self.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.body_color = body_color

    def draw(self):
        """Отрисовывает объект на экране"""
        raise NotImplementedError()


class Apple(GameObject):
    """Класс, представляющий яблоко."""

    def __init__(self):
        """Инициализация яблока."""
        super().__init__()
        self.randomize_position([])
        self.body_color = APPLE_COLOR

    def randomize_position(self, snake_positions):
        """Случайная позиция яблока."""
        while True:
            self.position = (
                random.randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            )
            if self.position not in [tuple(pos) for pos in snake_positions]:
                break

    def draw(self):
        """Перемещение яблока в случайную позицию."""
        rect = pg.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс, представляющий змейку."""

    def __init__(self, body_color: Tuple[int, int, int] = SNAKE_COLOR):
        """Инициализация змейки."""
        super().__init__(body_color=body_color)
        self.length = 1
        self.positions = [list(self.position)]
        self.direction = RIGHT
        self.next_direction = None

    def update_direction(self):
        """Обновление направления после нажатия на кнопку"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Перемещает змейку и обрабатывает столкновение."""
        head_x, head_y = self.positions[0]
        new_head_x = (head_x + self.direction[0] * GRID_SIZE) % SCREEN_WIDTH
        new_head_y = (head_y + self.direction[1] * GRID_SIZE) % SCREEN_HEIGHT

        new_head = (new_head_x, new_head_y)

        self.positions.insert(0, list(new_head))
        if len(self.positions) > self.length:
            self.positions.pop()

    def draw(self):
        """Рисование змейки."""
        for position in self.positions:
            head_rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
            pg.draw.rect(screen, self.body_color, head_rect)
            pg.draw.rect(screen, BORDER_COLOR, head_rect, 1)

    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        return tuple(self.positions[0])

    def reset(self):
        """Возвращение змейки в начальное положение."""
        self.positions = [[SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2]]
        self.length = 1
        self.direction = RIGHT
        self.next_direction_direction = None


def handle_keys(game_object):
    """Изменение направления движения."""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pg.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pg.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pg.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Основной цикл игры."""
    snake = Snake()
    apple = Apple()
    pg.init()

    while True:
        handle_keys(snake)
        snake.update_direction()

        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position(snake.positions)

        snake.move()

        if snake.get_head_position() in [
            tuple(pos) for pos in snake.positions[4:]
        ]:
            snake.reset()  # Добавление функции reset
            return

        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw()
        apple.draw()
        clock.tick(SPEED)
        pg.display.update()


if __name__ == '__main__':
    main()
