import pygame
import random


from utils import (
    generate_rounds,
    check_collision,
    clear_lines,
    draw_game_over,
    draw_block,
    draw_playfield,
    rotate_piece,
    merge_piece,
    calculate_ghost_position,
)

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 300, 600
BLOCK_SIZE = 30
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GHOST_COLOR = (0, 128, 0, 1)  # Ghost piece color with reduced opacity

# Define Tetromino shapes
SHAPES = [
    [[1, 1, 1, 1]],
    [[1, 1], [1, 1]],
    [[1, 1, 1], [0, 1, 0]],
    [[1, 1, 1], [1, 0, 0]],
    [[1, 1, 1], [0, 0, 1]],
    [[1, 1, 0], [0, 1, 1]],
    [[0, 1, 1], [1, 1, 0]],
]

# Initialize game variables
ROUNDS = 2
SHAPE_INDEX = 7
rounds = []

for _ in range(ROUNDS):
    rounds.extend(generate_rounds(SHAPE_INDEX))

# ALL_PIECES
game_over = False
playfield = [[0] * (WIDTH // BLOCK_SIZE) for _ in range(HEIGHT // BLOCK_SIZE)]
current_piece = SHAPES[rounds.pop(0)]
x, y = WIDTH // BLOCK_SIZE // 2 - 1, 0

# Create a Pygame window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tetris")


# Game loop
clock = pygame.time.Clock()

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                x -= 1
                if check_collision(playfield, current_piece, x, y):
                    x += 1
            if event.key == pygame.K_RIGHT:
                x += 1
                if check_collision(playfield, current_piece, x, y):
                    x -= 1
            if event.key == pygame.K_DOWN:
                y += 1
                if check_collision(playfield, current_piece, x, y):
                    y -= 1
            if event.key == pygame.K_UP:  # Handle rotation
                current_piece = rotate_piece(current_piece, playfield, x, y)

    y += 1
    if check_collision(playfield, current_piece, x, y):
        y -= 1
        playfield = merge_piece(current_piece, playfield, x, y)
        playfield = clear_lines(playfield, HEIGHT, WIDTH, BLOCK_SIZE)
        if rounds:
            shape_index = rounds.pop(0)
        else:
            game_over = True
        current_piece = SHAPES[shape_index]
        x, y = WIDTH // BLOCK_SIZE // 2 - 1, 0
        if check_collision(playfield, current_piece, x, y):
            game_over = True

    screen.fill(BLACK)
    draw_playfield(screen, playfield, BLOCK_SIZE, WHITE)
    ghost_y, ghost_piece = calculate_ghost_position(playfield, x, y, current_piece)

    # Draw the ghost piece at its fixed position
    for row_idx, row in enumerate(ghost_piece):
        for col_idx, cell in enumerate(row):
            if cell:
                pygame.draw.rect(
                    screen,
                    GHOST_COLOR,
                    (
                        (x + col_idx) * BLOCK_SIZE,
                        (ghost_y + row_idx) * BLOCK_SIZE,
                        BLOCK_SIZE,
                        BLOCK_SIZE,
                    ),
                )

    for row_idx, row in enumerate(current_piece):
        for col_idx, cell in enumerate(row):
            if cell:
                draw_block(screen, x + col_idx, y + row_idx, WHITE, BLOCK_SIZE)

    if game_over:
        screen = draw_game_over(screen, WIDTH, HEIGHT, WHITE)

    pygame.display.update()
    clock.tick(3)

pygame.quit()
