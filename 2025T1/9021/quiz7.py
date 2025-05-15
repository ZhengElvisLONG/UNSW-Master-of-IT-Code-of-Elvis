# Written by Zheng LONG for COMP9021
#
# Randomly fills an array of size 10x10 with True and False,
# displayed as black and white squares, respectively
# and outputs the minimal number of chess knights needed to jump
# from black square to black square and visit all black squares
# (they can jump back to locations previously visited).


from random import seed, randrange
import sys
from collections import deque
import numpy as np
from typing import Tuple
dim = 10

def display_grid():
    squares = np.array(['⬜', '⬛'])
    grid_np = np.array(grid)
    for row in grid_np:
        print('    ', ''.join(squares[row.astype(int)]))

def bfs(start, grid, dim, moves):
    """通用BFS函数，返回从start出发可达的所有连通节点"""
    visited = set()
    component = []
    queue = deque([start])
    visited.add(start)
    
    while queue:
        x, y = queue.popleft()
        component.append((x, y))
        for dx, dy in moves:
            nx, ny = x + dx, y + dy
            if 0 <= nx < dim and 0 <= ny < dim and grid[nx][ny] and (nx, ny) not in visited:
                visited.add((nx, ny))
                queue.append((nx, ny))
    return component

try:
    for_seed, n = map(int, input('Enter two integers: ').split())
    n = n or 1  # 如果n为0，则设为1
except ValueError:
    print('Incorrect input, giving up.')
    sys.exit()

# Check if n is within the range
seed(for_seed)
grid = [[randrange(abs(n)) == 0 if n < 0 else randrange(n) > 0 for _ in range(dim)] for _ in range(dim)]
print('Here is the grid that has been generated:')
display_grid()
print()

# 定义骑士的移动方向（8个可能的移动方向）
knight_moves = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]

# 检查坐标是否在网格范围内
def is_valid(point: Tuple[int, int], dim: int) -> bool:
    x, y = point
    return all(0 <= coord < dim for coord in (x, y))

# 使用BFS找出所有黑色方格的连通分量
def find_connected_components():
    black_squares = [(i, j) for i in range(dim) for j in range(dim) if grid[i][j]]
    if not black_squares:
        return 0
    
    visited = set()
    components = 0
    
    for square in black_squares:
        if square not in visited:
            component = bfs(square, grid, dim, knight_moves)
            visited.update(component)
            components += 1
    
    return components

# 计算并输出结果
num_knights = find_connected_components()

# 根据骑士数量输出不同的消息
if num_knights == 0:
    print('No chess knight has explored this board.')
elif num_knights == 1:
    print('At least 1 chess knight has explored this board.')
else:
    print(f'At least {num_knights} chess knights have explored this board.')
