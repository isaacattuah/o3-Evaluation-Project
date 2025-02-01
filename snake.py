import pygame
import sys
import random

# Initialize pygame
pygame.init()

# --- Game Configuration ---
# Screen dimensions (in pixels)
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 400

# Grid configuration: Each cell will be this many pixels square.
CELL_SIZE = 20
GRID_WIDTH = WINDOW_WIDTH // CELL_SIZE
GRID_HEIGHT = WINDOW_HEIGHT // CELL_SIZE

# Colors (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED   = (255, 0, 0)
GREEN = (0, 200, 0)
BLUE  = (0, 0, 255)

# Set up display and clock
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()

def draw_grid():
    """Draw grid lines to help visualize the game area."""
    for x in range(0, WINDOW_WIDTH, CELL_SIZE):
        pygame.draw.line(screen, BLACK, (x, 0), (x, WINDOW_HEIGHT))
    for y in range(0, WINDOW_HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, BLACK, (0, y), (WINDOW_WIDTH, y))

def random_position():
    """Return a random position within the grid as a (col, row) tuple."""
    return (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))

def main():
    # --- Initialize Game Variables ---
    # Snake starts at the center of the grid
    snake = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
    # Initial direction: moving up (0, -1). Direction is a tuple (dx, dy).
    direction = (0, -1)
    # The snake's initial length (it will grow as it eats apples)
    snake_length = 3

    # Spawn the first apple
    apple = random_position()
    while apple in snake:
        apple = random_position()

    game_over = False

    # --- Main Game Loop ---
    while not game_over:
        # Process events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Change direction based on arrow key input, preventing reversal
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != (0, 1):
                    direction = (0, -1)
                elif event.key == pygame.K_DOWN and direction != (0, -1):
                    direction = (0, 1)
                elif event.key == pygame.K_LEFT and direction != (1, 0):
                    direction = (-1, 0)
                elif event.key == pygame.K_RIGHT and direction != (-1, 0):
                    direction = (1, 0)

        # Calculate new head position based on current direction
        head_x, head_y = snake[0]
        dx, dy = direction
        new_head = (head_x + dx, head_y + dy)

        # Check for collision with the walls
        if (new_head[0] < 0 or new_head[0] >= GRID_WIDTH or
            new_head[1] < 0 or new_head[1] >= GRID_HEIGHT):
            game_over = True

        # Check for collision with itself
        if new_head in snake:
            game_over = True

        # Insert the new head at the beginning of the snake list
        snake.insert(0, new_head)

        # Check if the snake has eaten the apple
        if new_head == apple:
            snake_length += 1
            # Generate a new apple that is not on the snake
            apple = random_position()
            while apple in snake:
                apple = random_position()
        else:
            # Remove the tail segment if no apple was eaten, to keep snake the same length
            if len(snake) > snake_length:
                snake.pop()

        # --- Drawing ---
        screen.fill(WHITE)
        draw_grid()

        # Draw the apple
        apple_rect = pygame.Rect(apple[0] * CELL_SIZE, apple[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, RED, apple_rect)

        # Draw the snake: draw each segment as a rectangle.
        for segment in snake:
            segment_rect = pygame.Rect(segment[0] * CELL_SIZE, segment[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, GREEN, segment_rect)

        pygame.display.flip()

        # Control the game speed (frames per second)
        clock.tick(10)

    # --- Game Over Screen ---
    font = pygame.font.SysFont("Arial", 36)
    text = font.render("Game Over!", True, BLUE)
    text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
    screen.blit(text, text_rect)
    pygame.display.flip()
    pygame.time.wait(2000)
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
