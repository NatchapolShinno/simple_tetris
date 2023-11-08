import fun
import numpy as np
import copy

WIDTH, HEIGHT = 300, 600
BLOCK_SIZE = 30
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GHOST_COLOR = (0, 128, 0, 1)  # Ghost piece color with reduced opacity

PAFEMAP = [[0] * (WIDTH // BLOCK_SIZE) for _ in range(HEIGHT // BLOCK_SIZE)]
xlist = np.zeros(10)
rotationlist = np.zeros(10)

def search_perfect(current_map,piece,rotation_count,x,next):
    fun.playfield = copy.deepcopy(current_map)
    num = next[piece]
    fun.current_piece = fun.SHAPES[num][:] 
    cx, fun.y = WIDTH // BLOCK_SIZE // 2 - 1, 0
    fun.x = x
    check = 0
    #print(current_map)
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
            fun.merge_piece()
            fun.clear_lines()
    
    if fun.playfield == PAFEMAP:
        xlist[piece] = x
        rotationlist[piece] = rotation_count
        return 1
    
    # 全てのミノでパフェがとれない
    if piece == 9:
        return 0
    
    # 5段目より高い場合はパフェがとれない
    for i in range(10):
        if fun.playfield[15][i] == 1:
            return 0
    
    current_map = copy.deepcopy(fun.playfield)
    if piece < 5:
        print(piece,rotation_count,x)

    # 次のミノを置く
    if next[piece + 1] == 0 or next[piece + 1] == 5 or next[piece + 1] == 6:
        for i in range(10):
            for j in range(2):
                next_map = copy.deepcopy(current_map)
                if search_perfect(next_map,piece+1,j,i,next) == 1:
                    xlist[piece] = x
                    rotationlist[piece] = rotation_count
                    return 1
    elif next[piece + 1] == 1:
        for i in range(10):
            next_map = copy.deepcopy(current_map)
            if search_perfect(next_map,piece+1,0,i,next) == 1:
                xlist[piece] = x
                rotationlist[piece] = rotation_count
                return 1
    else:
        for i in range(10):
            #print(piece,rotation_count,x)
            for j in range(4):
                next_map = copy.deepcopy(current_map)
                if search_perfect(next_map,piece+1,j,i,next) == 1:
                    xlist[piece] = x
                    rotationlist[piece] = rotation_count
                    return 1
                
    return 0