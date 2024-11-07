import random
import pygame


# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """Базовый класс для игровый объектов."""

    def __init__(self, x=None, y=None, color=None, size=GRID_SIZE):
        """Инициализация GameObject"""
        self.x = x
        self.y = y
        self.color = color
        self.size = size
        self.rect = pygame.Rect(x, y, size, size)

    def draw(self):
        """Отрисовывает объект на экране"""
        pygame.draw.rect(screen, self.color, self.rect)
        pygame.draw.rect(screen, BORDER_COLOR, self.rect, 1)


class Apple(GameObject):
    """Класс, представляющий яблоко."""

    def __init__(self):
        """Инициализация яблока."""
        super().__init__(
            self.position_random_x(), self.position_random_y(), APPLE_COLOR
        )
        self.position = (self.x, self.y)
        self.body_color = APPLE_COLOR

    def position_random_x(self):
        """Случайная позиция относительно X."""
        return random.randint(0, GRID_WIDTH - 1) * GRID_SIZE

    def position_random_y(self):
        """Слуайная позиция относительно Y."""
        return random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE

    def respawn(self):
        """Перемещение яблока в случайную позицию."""
        self.x = self.position_random_x()
        self.y = self.position_random_y()
        self.rect = pygame.Rect(
            self.x, self.y, self.size, self.size
        )


class Snake(GameObject):
    """Класс, представляющий змейку."""

    def __init__(self):
        """Инициализация змейки."""
        super().__init__(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, SNAKE_COLOR)
        self.body = [(self.x, self.y)]
        self.direction = RIGHT
        self.next_direction = RIGHT
        self.positions = [(self.x, self.y)]
        self.body_color = SNAKE_COLOR
        self.length = 1

    def move(self):
        """Перемещает змейку и обрабатывает столкнование."""
        head_x, head_y = self.body[0]
        new_head_x = (head_x + self.direction[0] * GRID_SIZE)
        new_head_y = (head_y + self.direction[1] * GRID_SIZE)

        # Обработка границ
        if new_head_x < 0:
            new_head_x = SCREEN_WIDTH
        elif new_head_x >= SCREEN_WIDTH:
            new_head_x = (head_x + self.direction[0] * GRID_SIZE) % GRID_SIZE

        if new_head_y < 0:
            new_head_y = SCREEN_HEIGHT
        elif new_head_y >= SCREEN_HEIGHT:
            new_head_y = (head_y + self.direction[1] * GRID_SIZE) % GRID_SIZE

        if (new_head_x, new_head_y) in self.body:
            self.reset()  # Добавление функции reset
            return

        self.body.insert(0, (new_head_x, new_head_y))
        if len(self.body) > self.length:
            self.body.pop()
        self.direction = self.next_direction

    def draw(self):
        """Рисование змейки."""
        for x, y in self.body:
            pygame.draw.rect(screen, self.color, (x, y, GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(
                screen, BORDER_COLOR, (x, y, GRID_SIZE, GRID_SIZE), 1
            )

    def eating_apple(self, apple):
        """Поедание яблока змейкой."""
        if self.body[0] == (apple.x, apple.y):
            self.length += 1
            apple.respawn()
            return True
        return False

    def reset(self):
        """Возвращение змейки в начальное положение."""
        self.length = 1
        self.body = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = RIGHT
        self.next_direction = RIGHT


def handle_keys(snake):
    """Изменение направления движения."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake.direction != DOWN:
                snake.next_direction = UP
            elif event.key == pygame.K_DOWN and snake.direction != UP:
                snake.next_direction = DOWN
            elif event.key == pygame.K_LEFT and snake.direction != RIGHT:
                snake.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and snake.direction != LEFT:
                snake.next_direction = RIGHT


def main():
    """Основной цикл игры."""
    snake = Snake()
    apple = Apple()
    pygame.init()
    # Тут нужно создать экземпляры классов.

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.move()
        if snake.eating_apple(apple):
            pass
        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw()
        apple.draw()
        pygame.display.update()
    # Тут опишите основную логику игры.


if __name__ == '__main__':
    main()
