import random
from copy import deepcopy

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
    [[0, 1, 1], [1, 1, 0]],
    [[1, 1, 0], [0, 1, 1]],
]

# Initialize game variables
game_over = False
playfield = [[0] * (WIDTH // BLOCK_SIZE) for _ in range(HEIGHT // BLOCK_SIZE)]
current_piece = random.choice(SHAPES)
x, y = WIDTH // BLOCK_SIZE // 2 - 1, 0

def calculate_ghost_position():
    ghost_piece = deepcopy(current_piece)
    ghost_y = y
    while not check_collision(ghost_piece, x, ghost_y + 1):
        ghost_y += 1
    return ghost_y, ghost_piece

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

# Function to rotate the current piece
def rotate_piece():
    global current_piece
    rotated_piece = list(zip(*reversed(current_piece)))
    if not check_collision(rotated_piece, x, y):
        current_piece = rotated_piece