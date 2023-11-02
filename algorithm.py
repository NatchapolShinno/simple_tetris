import mo_tetris as tet
import numpy as np

WIDTH, HEIGHT = 300, 600
BLOCK_SIZE = 30
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GHOST_COLOR = (0, 128, 0, 1)  # Ghost piece color with reduced opacity

PAFEMAP = [[0] * (WIDTH // BLOCK_SIZE) for _ in range(HEIGHT // BLOCK_SIZE)]
current_map = [[0] * (WIDTH // BLOCK_SIZE) for _ in range(HEIGHT // BLOCK_SIZE)]
xlist = np.zeros(10)
rotationlist = np.zeros(10)

def search_perfect(current_map,piece,rotation_count,x):
    playfield = current_map
    current_piece = piece # 後でcurrent_piece = next[piece]に修正
    cx, y = WIDTH // BLOCK_SIZE // 2 - 1, 0
    
    # ゲームオーバーの判定
    if tet.check_collision(current_piece, cx, y):
        return 0

    # 決められた回数回転
    for i in range (rotation_count):
        tet.rotate_piece()
        
    # xの位置まで横に動けるかの判定
    if tet.check_collision(current_piece, x, y):
        return 0

    while not tet.check_collision(current_piece, x, y):
        y += 1
        if tet.check_collision(current_piece, x, y):
            y -= 1
            tet.merge_piece()
            tet.clear_lines()
    
    if playfield == PAFEMAP:
        xlist[piece] = x
        rotationlist[piece] = rotation_count
        return 1
    
    # 全てのミノでパフェがとれない
    if piece == 13:
        return 0
    
    next_map = playfield

    # 次のミノを置く
    if search_perfect(next_map,piece+1,0,0) == 1:
        xlist[piece] = x
        rotationlist[piece] = rotation_count
        return 1
    
    if search_perfect(next_map,piece+1,1,0) == 1:
        xlist[piece] = x
        rotationlist[piece] = rotation_count
        return 1
    
    if search_perfect(next_map,piece+1,2,0) == 1:
        xlist[piece] = x
        rotationlist[piece] = rotation_count
        return 1
    
    if search_perfect(next_map,piece+1,3,0) == 1:
        xlist[piece] = x
        rotationlist[piece] = rotation_count
        return 1
    
    if search_perfect(next_map,piece+1,0,1) == 1:
        xlist[piece] = x
        rotationlist[piece] = rotation_count
        return 1
    
    if search_perfect(next_map,piece+1,1,1) == 1:
        xlist[piece] = x
        rotationlist[piece] = rotation_count
        return 1
    
    if search_perfect(next_map,piece+1,2,1) == 1:
        xlist[piece] = x
        rotationlist[piece] = rotation_count
        return 1
    
    if search_perfect(next_map,piece+1,3,1) == 1:
        xlist[piece] = x
        rotationlist[piece] = rotation_count
        return 1
    
    if search_perfect(next_map,piece+1,0,2) == 1:
        xlist[piece] = x
        rotationlist[piece] = rotation_count
        return 1
    
    if search_perfect(next_map,piece+1,1,2) == 1:
        xlist[piece] = x
        rotationlist[piece] = rotation_count
        return 1
    
    if search_perfect(next_map,piece+1,2,2) == 1:
        xlist[piece] = x
        rotationlist[piece] = rotation_count
        return 1
    
    if search_perfect(next_map,piece+1,3,2) == 1:
        xlist[piece] = x
        rotationlist[piece] = rotation_count
        return 1
    
    if search_perfect(next_map,piece+1,0,3) == 1:
        xlist[piece] = x
        rotationlist[piece] = rotation_count
        return 1
    
    if search_perfect(next_map,piece+1,1,3) == 1:
        xlist[piece] = x
        rotationlist[piece] = rotation_count
        return 1
    
    if search_perfect(next_map,piece+1,2,3) == 1:
        xlist[piece] = x
        rotationlist[piece] = rotation_count
        return 1
    
    if search_perfect(next_map,piece+1,3,3) == 1:
        xlist[piece] = x
        rotationlist[piece] = rotation_count
        return 1
    
    if search_perfect(next_map,piece+1,0,4) == 1:
        xlist[piece] = x
        rotationlist[piece] = rotation_count
        return 1
    
    if search_perfect(next_map,piece+1,1,4) == 1:
        xlist[piece] = x
        rotationlist[piece] = rotation_count
        return 1
    
    if search_perfect(next_map,piece+1,2,4) == 1:
        xlist[piece] = x
        rotationlist[piece] = rotation_count
        return 1
    
    if search_perfect(next_map,piece+1,3,4) == 1:
        xlist[piece] = x
        rotationlist[piece] = rotation_count
        return 1
    
    if search_perfect(next_map,piece+1,0,5) == 1:
        xlist[piece] = x
        rotationlist[piece] = rotation_count
        return 1
    
    if search_perfect(next_map,piece+1,1,5) == 1:
        xlist[piece] = x
        rotationlist[piece] = rotation_count
        return 1
    
    if search_perfect(next_map,piece+1,2,5) == 1:
        xlist[piece] = x
        rotationlist[piece] = rotation_count
        return 1
    
    if search_perfect(next_map,piece+1,3,5) == 1:
        xlist[piece] = x
        rotationlist[piece] = rotation_count
        return 1
    
    if search_perfect(next_map,piece+1,0,6) == 1:
        xlist[piece] = x
        rotationlist[piece] = rotation_count
        return 1
    
    if search_perfect(next_map,piece+1,1,6) == 1:
        xlist[piece] = x
        rotationlist[piece] = rotation_count
        return 1
    
    if search_perfect(next_map,piece+1,2,6) == 1:
        xlist[piece] = x
        rotationlist[piece] = rotation_count
        return 1
    
    if search_perfect(next_map,piece+1,3,6) == 1:
        xlist[piece] = x
        rotationlist[piece] = rotation_count
        return 1
    
    if search_perfect(next_map,piece+1,0,7) == 1:
        xlist[piece] = x
        rotationlist[piece] = rotation_count
        return 1
    
    if search_perfect(next_map,piece+1,1,7) == 1:
        xlist[piece] = x
        rotationlist[piece] = rotation_count
        return 1
    
    if search_perfect(next_map,piece+1,2,7) == 1:
        xlist[piece] = x
        rotationlist[piece] = rotation_count
        return 1
    
    if search_perfect(next_map,piece+1,3,7) == 1:
        xlist[piece] = x
        rotationlist[piece] = rotation_count
        return 1
    
    if search_perfect(next_map,piece+1,0,8) == 1:
        xlist[piece] = x
        rotationlist[piece] = rotation_count
        return 1
    
    if search_perfect(next_map,piece+1,1,8) == 1:
        xlist[piece] = x
        rotationlist[piece] = rotation_count
        return 1
    
    if search_perfect(next_map,piece+1,2,8) == 1:
        xlist[piece] = x
        rotationlist[piece] = rotation_count
        return 1
    
    if search_perfect(next_map,piece+1,3,8) == 1:
        xlist[piece] = x
        rotationlist[piece] = rotation_count
        return 1
    
    if search_perfect(next_map,piece+1,0,9) == 1:
        xlist[piece] = x
        rotationlist[piece] = rotation_count
        return 1
    
    if search_perfect(next_map,piece+1,1,9) == 1:
        xlist[piece] = x
        rotationlist[piece] = rotation_count
        return 1
    
    if search_perfect(next_map,piece+1,2,9) == 1:
        xlist[piece] = x
        rotationlist[piece] = rotation_count
        return 1
    
    if search_perfect(next_map,piece+1,3,9) == 1:
        xlist[piece] = x
        rotationlist[piece] = rotation_count
        return 1
    
    return 0