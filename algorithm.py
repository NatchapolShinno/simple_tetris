import fun
import numpy as np
import copy

WIDTH, HEIGHT = 300, 600
BLOCK_SIZE = 30
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GHOST_COLOR = (0, 128, 0, 1)  # Ghost piece color with reduced opacity

PAFEMAP = [[0] * (WIDTH // BLOCK_SIZE) for _ in range(HEIGHT // BLOCK_SIZE)]
current_map = [[0] * (WIDTH // BLOCK_SIZE) for _ in range(HEIGHT // BLOCK_SIZE)]
xlist = np.zeros(10)
rotationlist = np.zeros(10)

def search_perfect(current_map,piece,rotation_count,x,next):
    fun.playfield = copy.deepcopy(current_map)
    num = next[piece]
    fun.current_piece = fun.SHAPES[num][:] 
    cx, fun.y = WIDTH // BLOCK_SIZE // 2 - 1, 0
    fun.x = x
    check = 0
    #print(piece,rotation_count,x)
    
    # ゲームオーバーの判定
    if fun.check_collision(fun.current_piece, cx, fun.y):
        return 0
    
    # 決められた回数回転
    for i in range (rotation_count):
        fun.rotate_piece()
        
    # xの位置まで横に動けるかの判定
    if fun.check_collision(fun.current_piece, fun.x, fun.y):
        return 0
    
    while check == 0:
        fun.y += 1
        if fun.check_collision(fun.current_piece, fun.x, fun.y):
            fun.y -= 1
            check = 1
            fun.merge_piece(current_map)
            fun.clear_lines()
    
    if current_map == PAFEMAP:
        xlist[piece] = x
        rotationlist[piece] = rotation_count
        return 1
    
    # 全てのミノでパフェがとれない
    if piece == 9:
        return 0
    
    # 次のミノを置く
    for i in range(10):
        #print(piece,rotation_count,x)
        for j in range(4):
            next_map = copy.deepcopy(current_map)
            if search_perfect(next_map,piece+1,j,i,next) == 1:
                xlist[piece] = x
                rotationlist[piece] = rotation_count
                return 1
    
    return 0