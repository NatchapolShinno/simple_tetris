import algorithm2 as algo
import time

WIDTH, HEIGHT = 300, 600
BLOCK_SIZE = 30
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GHOST_COLOR = (0, 128, 0, 1)  # Ghost piece color with reduced opacity
STARTMAP = [[0] * (WIDTH // BLOCK_SIZE) for _ in range(HEIGHT // BLOCK_SIZE)]
next = [3,5,0,2,6,1,4,2,3,4,1,6,5,0]
a = 0

start = time.time()
for i in range(10):
    for j in range(4):
        if algo.search_perfect(STARTMAP,0,j,i,next) == 1:
            a = 1

    if a == 1:
        break

print("a = ")
print(a)
print(algo.xlist)
print(algo.rotationlist)
end = time.time()
print(end - start)