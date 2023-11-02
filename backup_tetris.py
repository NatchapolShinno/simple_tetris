import pygame
import random
import copy

# Define colors
BLACK = (54, 57, 65)
WHITE = (220, 220, 220)
RED = (235, 79, 100)
GREEN = (81, 184, 77)
BLUE = (17, 101, 181)
YELLOW = (246, 208, 60)
CYAN = (66, 175, 225)
MAGENTA = (151, 57, 162)
ORANGE = (243, 137, 39)
GHOST_COLOR = (255, 255, 255,0.1)

# Define tetrominos without colors
tetrominos = [
    [[1, 1, 1, 1]],        # I-Mino
    [[1, 1, 1], [0, 1, 0]],    # T-Mino
    [[1, 1, 1], [1, 0, 0]],    # L-Mino
    [[1, 1, 1], [0, 0, 1]],    # J-Mino
    [[0, 1, 1], [1, 1, 0]],    # S-Mino
    [[1, 1, 0], [0, 1, 1]],    # Z-Mino
    [[1, 1], [1, 1]]        # O-Mino
]
# Define colors for each tetromino
tetromino_colors = {
    0: CYAN,    # I-Mino
    1: MAGENTA,  # T-Mino
    2: ORANGE,   # L-Mino
    3: BLUE,  # J-Mino
    4: GREEN,   # S-Mino
    5: RED,  # Z-Mino
    6: YELLOW  # O-Mino
}

# Define the fixed order of tetrominos
fixed_order_tetrominos = [0, 1, 2, 3, 4, 5, 6]  # Change the order as needed

next_mino_index = 0  # Initialize the index to track the next tetromino

# Define a variable to store the held tetromino
held_mino = None
can_hold = True  # Allow holding at the start of the game

# Set up the grid and window
block_size = 30
width = 10
height = 20
win_width = block_size * width
win_height = block_size * height
grid = [[0 for _ in range(width)] for _ in range(height)]

# Initialize Pygame
pygame.init()
win = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption("Tetris")

clock = pygame.time.Clock()


def draw_block(x, y, color):
    pygame.draw.rect(win, color, (x * block_size, y *
                     block_size, block_size, block_size))
    pygame.draw.rect(win, WHITE, (x * block_size, y *
                     block_size, block_size, block_size), 1)


def draw_grid():
    for y, row in enumerate(grid):
        for x, val in enumerate(row):
            if val:
                draw_block(x, y, val)


def new_mino():
    return random.choice(tetrominos)
# def new_mino():
#     global next_mino_index
#     current_mino = tetrominos[fixed_order_tetrominos[next_mino_index]]
#     next_mino_index = (next_mino_index + 1) % len(fixed_order_tetrominos)
#     return current_mino

def collide(current_mino, x, y):
    for row_index, row in enumerate(current_mino):
        for col_index, val in enumerate(row):
            if val:
                grid_row = y + row_index
                grid_col = x + col_index
                if not 0 <= grid_row < height or not 0 <= grid_col < width or grid[grid_row][grid_col]:
                    return True
    return False


def merge(current_mino, x, y, color):
    for row_index, row in enumerate(current_mino):
        for col_index, val in enumerate(row):
            if val:
                grid[y + row_index][x + col_index] = color


def clear_rows():
    global grid
    full_rows = [row for row in range(height) if 0 not in grid[row]]
    for row in full_rows:
        del grid[row]
        grid.insert(0, [0 for _ in range(width)])


def game_over():
    font = pygame.font.SysFont(None, 48)
    text = font.render("Game Over", True, WHITE)
    win.blit(text, (win_width // 2 - text.get_width() //
             2, win_height // 2 - text.get_height() // 2))
    pygame.display.update()
    pygame.time.wait(10000)

def game_clear():
    font = pygame.font.SysFont(None, 36)
    text = font.render("Congratulations", True, WHITE)
    win.blit(text, (win_width // 2 - text.get_width() //
             2, win_height // 2 - text.get_height() // 2))
    pygame.display.update()
    pygame.time.wait(10000)


def hold(current_mino):
    global held_mino, can_hold
    if can_hold:  # Allow holding only once per tetromino
        if held_mino is None:
            held_mino = current_mino
            current_mino = new_mino()
        else:
            held_mino, current_mino = current_mino, held_mino
        can_hold = False  # Disallow holding until next tetromino
    return current_mino


def instant_drop(current_mino, x, y):
    new_y = y
    while not collide(current_mino, x, new_y + 1):
        new_y += 1
    return x, new_y

def handle_input(current_mino, x, y, current_color):
    instant_dropped = False  # Initialize instant_dropped outside the event loop

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return True, x, y, current_mino, current_color
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and not collide(current_mino, x - 1, y):
                x -= 1
            if event.key == pygame.K_RIGHT and not collide(current_mino, x + 1, y):
                x += 1
            if event.key == pygame.K_DOWN and not collide(current_mino, x, y + 1):
                y += 1
            if event.key == pygame.K_UP:
                rotated_mino = list(zip(*current_mino[::-1]))
                if not collide(rotated_mino, x, y):
                    current_mino = rotated_mino
            if event.key == pygame.K_SPACE and not instant_dropped:  # Space key for instant drop
                x, y = instant_drop(current_mino, x, y)
                instant_dropped = True
    return False, x, y, current_mino, current_color


# (Previous code remains the same)

def get_mino_type(current_mino):
    for i, shape in enumerate(tetrominos):
        if shape == current_mino:
            return i
    return None


def is_perfect_clear():
    for row in grid:
        if any(row):
            return False  # If any row has blocks, it's not a perfect clear
    return True


def calculate_ghost_position(current_mino, x, y):
    ghost_y = y
    ghost_piece = copy.deepcopy(current_mino)

    while not collide(ghost_piece, x, ghost_y + 1):
        ghost_y += 1

    return ghost_y, ghost_piece


def draw_ghost_piece(current_mino, x, y):
    ghost_y, ghost_piece = calculate_ghost_position(current_mino, x, y)

    for row_idx, row in enumerate(ghost_piece):
        for col_idx, cell in enumerate(row):
            if cell:
                pygame.draw.rect(win, GHOST_COLOR, ((
                    x + col_idx) * block_size, (ghost_y + row_idx) * block_size, block_size, block_size))

def game():
    current_mino = new_mino()
    current_mino_color = tetromino_colors[get_mino_type(current_mino)]
    x, y = width // 2 - len(current_mino[0]) // 2, 0
    game_over_flag = False
    clock = pygame.time.Clock()
    time_elapsed = 0
    speed = 1  # Controls the speed of falling pieces

    while not game_over_flag:
        win.fill(BLACK)
        game_over_flag, x, y, current_mino, current_mino_color = handle_input(
            current_mino, x, y, current_mino_color)
        draw_ghost_piece(current_mino, x, y)
        if not game_over_flag:
            time_elapsed += clock.get_rawtime()
            clock.tick()
            if time_elapsed / 1000 > speed:  # Change the speed of falling pieces
                if not collide(current_mino, x, y + 1):
                    y += 1
                else:
                    merge(current_mino, x, y, current_mino_color)
                    clear_rows()
                    if is_perfect_clear():
                        # If it's a perfect clear, end the game
                        game_over_flag = True
                        game_clear()
                    current_mino = new_mino()
                    current_mino_color = tetromino_colors[get_mino_type(
                        current_mino)]
                    x, y = width // 2 - len(current_mino[0]) // 2, 0
                    if collide(current_mino, x, y):
                        game_over_flag = True
                        game_over()
                time_elapsed = 0

            draw_grid()
            for row_index, row in enumerate(current_mino):
                for col_index, val in enumerate(row):
                    if val:
                        draw_block(x + col_index, y + row_index,
                                   current_mino_color)

            pygame.display.update()

    pygame.quit()


game()
