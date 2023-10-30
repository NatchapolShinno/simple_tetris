import pygame
import random
from copy import deepcopy

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
]

# Initialize game variables
game_over = False
playfield = [[0] * (WIDTH // BLOCK_SIZE) for _ in range(HEIGHT // BLOCK_SIZE)]
current_piece = random.choice(SHAPES)
x, y = WIDTH // BLOCK_SIZE // 2 - 1, 0

# Create a Pygame window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tetris")

def calculate_ghost_position():
    ghost_piece = deepcopy(current_piece)
    ghost_y = y
    while not check_collision(ghost_piece, x, ghost_y + 1):
        ghost_y += 1
    return ghost_y, ghost_piece

# Function to draw the ghost piece
def draw_ghost_piece():
    ghost_y, ghost_piece = calculate_ghost_position()
    for row_idx, row in enumerate(ghost_piece):
        for col_idx, cell in enumerate(row):
            if cell:
                pygame.draw.rect(screen, GHOST_COLOR, ((x + col_idx) * BLOCK_SIZE, (ghost_y + row_idx) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

# Function to draw a block
def draw_block(x, y):
    pygame.draw.rect(screen, WHITE, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

# Function to draw the playfield
def draw_playfield():
    for row in range(len(playfield)):
        for col in range(len(playfield[row])):
            if playfield[row][col]:
                draw_block(col, row)

# Function to check collision for a given piece
def check_collision(piece, piece_x, piece_y):
    for row_idx, row in enumerate(piece):
        for col_idx, cell in enumerate(row):
            if cell:
                if piece_y + row_idx >= len(playfield) or piece_x + col_idx < 0 or piece_x + col_idx >= len(playfield[0]) or playfield[piece_y + row_idx][piece_x + col_idx]:
                    return True
    return False

# Function to merge the current piece into the playfield
def merge_piece():
    for row_idx, row in enumerate(current_piece):
        for col_idx, cell in enumerate(row):
            if cell:
                playfield[y + row_idx][x + col_idx] = 1

# Function to clear completed lines
def clear_lines():
    global playfield
    playfield = [row for row in playfield if not all(row)]
    while len(playfield) < HEIGHT // BLOCK_SIZE:
        playfield.insert(0, [0] * (WIDTH // BLOCK_SIZE))

# Function to draw "Game Over" text
def draw_game_over():
    font = pygame.font.Font(None, 36)
    text = font.render("Game Over", True, WHITE)
    screen.blit(text, (WIDTH // 2 - 100, HEIGHT // 2 - 18))

# Function to rotate the current piece
def rotate_piece():
    global current_piece
    rotated_piece = list(zip(*reversed(current_piece)))
    if not check_collision(rotated_piece, x, y):
        current_piece = rotated_piece

# Game loop
clock = pygame.time.Clock()

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                x -= 1
                if check_collision(current_piece, x, y):
                    x += 1
            if event.key == pygame.K_RIGHT:
                x += 1
                if check_collision(current_piece, x, y):
                    x -= 1
            if event.key == pygame.K_DOWN:
                y += 1
                if check_collision(current_piece, x, y):
                    y -= 1
            if event.key == pygame.K_UP:  # Handle rotation
                rotate_piece()

    y += 1
    if check_collision(current_piece, x, y):
        y -= 1
        merge_piece()
        clear_lines()
        current_piece = random.choice(SHAPES)
        x, y = WIDTH // BLOCK_SIZE // 2 - 1, 0
        if check_collision(current_piece, x, y):
            game_over = True

    screen.fill(BLACK)
    draw_playfield()
    ghost_y, ghost_piece = calculate_ghost_position()
    
    # Draw the ghost piece at its fixed position
    for row_idx, row in enumerate(ghost_piece):
        for col_idx, cell in enumerate(row):
            if cell:
                pygame.draw.rect(screen, GHOST_COLOR, ((x + col_idx) * BLOCK_SIZE, (ghost_y + row_idx) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

    for row_idx, row in enumerate(current_piece):
        for col_idx, cell in enumerate(row):
            if cell:
                draw_block(x + col_idx, y + row_idx)

    if game_over:
        draw_game_over()

    pygame.display.update()
    clock.tick(5)

pygame.quit()