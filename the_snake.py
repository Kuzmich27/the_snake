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

    def __init__(self) -> None:
        """Инициализация GameObject"""
        self.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.body_color = None

    def draw(self):
        """Отрисовывает объект на экране"""
        pass


class Apple(GameObject):
    """Класс, представляющий яблоко."""

    def __init__(self):
        """Инициализация яблока."""
        super().__init__()
        self.randomize_position()
        self.body_color = APPLE_COLOR

    def randomize_position(self):
        """Случайная позиция яблока."""
        self.position = (
            random.randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        )

    def draw(self):
        """Перемещение яблока в случайную позицию."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс, представляющий змейку."""

    def __init__(self):
        """Инициализация змейки."""
        super().__init__()
        self.length = 1
        self.positions = [list(self.position)]
        self.direction = RIGHT
        self.next_direction = None
        self.body_color = SNAKE_COLOR

    def update_direction(self):
        """Обновление направления после нажатия на кнопку"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Перемещает змейку и обрабатывает столкнование."""
        head_x, head_y = self.positions[0]
        new_head_x = head_x + self.direction[0] * GRID_SIZE
        new_head_y = head_y + self.direction[1] * GRID_SIZE

        # Обработка границ
        if new_head_x < 0:
            new_head_x = SCREEN_WIDTH
        elif new_head_x >= SCREEN_WIDTH:
            new_head_x = (head_x + self.direction[0] * GRID_SIZE) % GRID_SIZE

        if new_head_y < 0:
            new_head_y = SCREEN_HEIGHT
        elif new_head_y >= SCREEN_HEIGHT:
            new_head_y = (head_y + self.direction[1] * GRID_SIZE) % GRID_SIZE

        new_head = (new_head_x, new_head_y)

        if new_head in [tuple(pos) for pos in self.positions[1:]]:
            self.reset()  # Добавление функции reset
            return

        self.positions.insert(0, list(new_head))
        if len(self.positions) > self.length:
            self.positions.pop()

    def draw(self):
        """Рисование змейки."""
        for posit in self.positions:
            head_rect = pygame.Rect(posit, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, head_rect)
            pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

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
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Основной цикл игры."""
    snake = Snake()
    apple = Apple()
    pygame.init()
    # Тут нужно создать экземпляры классов.
    running = True

    while running:
        handle_keys(snake)
        snake.update_direction()

        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()

        snake.move()

        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw()
        apple.draw()
        clock.tick(SPEED)
        pygame.display.update()
    # Тут опишите основную логику игры.


if __name__ == '__main__':
    main()
