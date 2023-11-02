import random
import pygame
from copy import deepcopy


def generate_rounds(N):
    round_array = list(range(N))
    random.shuffle(round_array)
    return round_array


def calculate_ghost_position(playfield, x, y, current_piece):
    ghost_piece = deepcopy(current_piece)
    ghost_y = y
    while not check_collision(playfield, ghost_piece, x, ghost_y + 1):
        ghost_y += 1
    return ghost_y, ghost_piece


def draw_ghost_piece(screen, playfield, x, y, current_piece, color, block_size):
    ghost_y, ghost_piece = calculate_ghost_position(playfield, x, y, current_piece)
    for row_idx, row in enumerate(ghost_piece):
        for col_idx, cell in enumerate(row):
            if cell:
                pygame.draw.rect(
                    screen,
                    color,
                    (
                        (x + col_idx) * block_size,
                        (ghost_y + row_idx) * block_size,
                        block_size,
                        block_size,
                    ),
                )


def draw_block(screen, x, y, color, block_size):
    pygame.draw.rect(
        screen, color, (x * block_size, y * block_size, block_size, block_size)
    )


def draw_playfield(screen, playfield, block_size, color):
    for y, row in enumerate(playfield):
        for x, cell in enumerate(row):
            if cell:
                draw_block(screen, x, y, color, block_size)


def check_collision(playfield, piece, piece_x, piece_y):
    for row_idx, row in enumerate(piece):
        for col_idx, cell in enumerate(row):
            if cell:
                if (
                    piece_y + row_idx >= len(playfield)
                    or piece_x + col_idx < 0
                    or piece_x + col_idx >= len(playfield[0])
                    or playfield[piece_y + row_idx][piece_x + col_idx]
                ):
                    return True
    return False


def merge_piece(current_piece, playfield, x, y):
    for row_idx, row in enumerate(current_piece):
        for col_idx, cell in enumerate(row):
            if cell:
                playfield[y + row_idx][x + col_idx] = 1

    return playfield


def clear_lines(playfield, height, width, block_size):
    playfield = [row for row in playfield if not all(row)]
    while len(playfield) < height // block_size:
        playfield.insert(0, [0] * (width // block_size))
    return playfield


def draw_game_over(screen, width, height, color):
    font = pygame.font.Font(None, 36)
    text = font.render("Game Over", True, color)
    screen.blit(text, (width // 2 - 100, height // 2 - 18))

    return screen


def rotate_piece(current_piece, playfield, x, y):
    rotated_piece = list(zip(*reversed(current_piece)))
    if not check_collision(playfield, rotated_piece, x, y):
        return rotated_piece
    return current_piece
