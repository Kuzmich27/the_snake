import random
from typing import Optional

import pygame as pg


# Константы для размеров поля и сетки:
SCREEN_WIDTH: int = 640
SCREEN_HEIGHT: int = 480
GRID_SIZE: int = 20
GRID_WIDTH: int = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT: int = SCREEN_HEIGHT // GRID_SIZE

# Создаем алиас для типа
DIRECTION = tuple[int, int]
POSITION = tuple[int, int]
COLOR = tuple[int, int, int]

# Направления движения:
UP: DIRECTION = (0, -1)
DOWN: DIRECTION = (0, 1)
LEFT: DIRECTION = (-1, 0)
RIGHT: DIRECTION = (1, 0)

# Цвет стандартный - белый:
DEFOLT_COLOR: COLOR = (255, 255, 255)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR: COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR: COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR: COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR: COLOR = (0, 255, 0)

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

    def __init__(self, body_color: COLOR = DEFOLT_COLOR):
        """Инициализация GameObject"""
        self.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.body_color = body_color

    def draw(self):
        """Отрисовывает объект на экране"""
        raise NotImplementedError('Метод draw пока не был реализован')


class Apple(GameObject):
    """Класс, представляющий яблоко."""

    def __init__(self, body_color=APPLE_COLOR,
                 occupied_positions: Optional[list[POSITION]] = None):
        """Инициализация яблока."""
        super().__init__(body_color)
        if occupied_positions is None:
            occupied_positions = []
        self.randomize_position(occupied_positions)

    def randomize_position(self, occupied_positions: list[POSITION]):
        """Случайная позиция яблока."""
        while True:
            self.position = (
                random.randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            )
            if self.position not in occupied_positions:
                break

    def draw(self):
        """Перемещение яблока в случайную позицию."""
        rect = pg.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс, представляющий змейку."""

    def __init__(self, body_color: COLOR = SNAKE_COLOR):
        """Инициализация змейки."""
        super().__init__(body_color)
        self.length = 1
        self.positions = [(self.position)]
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

        self.positions.insert(0, tuple(new_head))
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
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.length = 1
        self.direction = RIGHT
        self.next_direction = None


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
    apple = Apple(occupied_positions=snake.positions)
    pg.init()

    while True:
        handle_keys(snake)
        snake.update_direction()

        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position(snake.positions)

        snake.move()

        if snake.get_head_position() in snake.positions[4:]:
            snake.reset()  # Добавление функции reset
            apple.randomize_position(snake.positions)

        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw()
        apple.draw()
        clock.tick(SPEED)
        pg.display.update()


if __name__ == '__main__':
    main()
