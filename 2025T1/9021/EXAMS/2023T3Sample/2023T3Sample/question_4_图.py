#  You can assume that i and j are both between 0 and 9 included.
#  i is the row number (indexed from top to bottom),
#  j is the column number (indexed from left to right)
#  of the displayed grid.
    

from random import seed, randrange


def area(for_seed, sparsity, i, j):
    '''
    >>> area(0, 1, 5, 5)
    The grid is:
    1 1 1 1 1 1 1 1 1 1
    1 1 1 1 1 1 1 1 1 1
    1 1 1 1 1 1 1 1 1 1
    1 1 1 1 1 1 1 1 1 1
    1 1 1 1 1 1 1 1 1 1
    1 1 1 1 1 1 1 1 1 1
    1 1 1 1 1 1 1 1 1 1
    1 1 1 1 1 1 1 1 1 1
    1 1 1 1 1 1 1 1 1 1
    1 1 1 1 1 1 1 1 1 1
    The area of the largest empty region of the grid
    containing the point (5, 5) is: 0
    >>> area(0, 1000, 5, 5)
    The grid is:
    0 0 0 0 0 0 0 0 0 0
    0 0 0 0 0 0 0 0 0 0
    0 0 0 0 0 0 0 0 0 0
    0 0 0 0 0 0 0 0 0 0
    0 0 0 0 0 0 0 0 0 0
    0 0 0 0 0 0 0 0 0 0
    0 0 0 0 0 0 0 0 0 0
    0 0 0 0 0 0 0 0 0 0
    0 0 0 0 0 0 0 0 0 0
    0 0 0 0 0 0 0 0 0 0
    The area of the largest empty region of the grid
    containing the point (5, 5) is: 100
    >>> area(0, 3, 6, 2)
    The grid is:
    0 0 1 0 0 0 0 0 0 0
    0 1 0 1 0 1 1 0 0 0
    0 0 1 0 1 0 1 0 0 0
    0 1 0 0 0 0 0 1 0 0
    0 0 0 1 0 1 1 0 0 0
    0 0 1 0 0 0 1 0 0 0
    1 1 0 1 1 1 0 0 1 1
    0 0 0 1 0 0 0 0 1 0
    0 0 1 0 0 0 0 0 1 0
    0 0 0 1 0 1 1 1 1 0
    The area of the largest empty region of the grid
    containing the point (6, 2) is: 9
    >>> area(0, 2, 9, 5)
    The grid is:
    0 0 1 0 0 0 0 0 0 1
    1 0 1 1 0 1 0 1 1 0
    0 1 0 0 0 1 0 0 0 1
    1 1 0 1 0 0 1 0 1 1
    1 1 1 0 1 1 0 0 1 0
    0 1 0 1 0 0 1 0 0 1
    0 1 1 1 1 0 0 1 1 1
    1 1 1 0 0 1 1 0 0 0
    0 0 1 0 1 0 0 1 1 1
    0 1 1 0 1 0 0 1 1 1
    The area of the largest empty region of the grid
    containing the point (9, 5) is: 4
    >>> area(0, 2, 2, 7)
    The grid is:
    0 0 1 0 0 0 0 0 0 1
    1 0 1 1 0 1 0 1 1 0
    0 1 0 0 0 1 0 0 0 1
    1 1 0 1 0 0 1 0 1 1
    1 1 1 0 1 1 0 0 1 0
    0 1 0 1 0 0 1 0 0 1
    0 1 1 1 1 0 0 1 1 1
    1 1 1 0 0 1 1 0 0 0
    0 0 1 0 1 0 0 1 1 1
    0 1 1 0 1 0 0 1 1 1
    The area of the largest empty region of the grid
    containing the point (2, 7) is: 22
    >>> area(0, 4, 2, 7)
    The grid is:
    0 0 1 0 0 0 0 0 0 0
    0 0 0 1 0 0 0 1 1 0
    0 1 0 0 0 0 0 0 0 1
    1 1 0 1 0 0 0 0 1 0
    0 0 0 0 1 1 0 0 1 0
    0 1 0 0 0 0 1 0 0 0
    0 0 0 0 1 0 0 1 1 0
    0 1 1 0 0 0 0 0 0 0
    0 0 1 0 1 0 0 0 0 1
    0 1 0 0 0 0 0 1 1 0
    The area of the largest empty region of the grid
    containing the point (2, 7) is: 73
    '''
    seed(for_seed)
    grid = [[int(randrange(sparsity) == 0) for _ in range(10)]
                for _ in range(10)
           ]
    print('The grid is:')
    for row in grid:
        print(*row)
    print('The area of the largest empty region of the grid')
    print(f'containing the point ({i}, {j}) is: ', end='')
    # INSERT YOUR CODE HERE
    # '''
    # grid_copy = grid 只是创建引用，不是真正的拷贝
    # 应该使用深拷贝：grid_copy = [row[:] for row in grid]
    # '''
    # grid_copy = [row[:] for row in grid]
    # def dfs(grid_copy, i, j):
    #     if i > 9 or j > 9 or i < 0 or j < 0 or grid_copy[i][j] == 1:
    #         return False
    #     grid_copy[i][j] = 1
    #     if dfs(grid_copy, i + 1, j) or dfs(grid_copy, i - 1, j) or dfs(grid_copy, i, j + 1) or dfs(grid_copy, i ,j - 1):
    #         return True
    #     '''这个是计数的，所以不需要回溯'''
    #     # grid_copy[i][j] = 0
    #     return False
    # dfs(grid_copy, i, j)
    # num = 0
    # for i in range(10):
    #     for j in range(10):
    #         if grid_copy[i][j] - grid[i][j] == 1:
    #             num += 1
    # print(num)

# POSSIBLY DEFINE OTHER FUNCTIONS
    grid_path = [[1 for _ in range(10)] for _ in range(10)]
    # grid_copy = [[1 for _ in range(10)] for _ in range(10)]
    # for x in range(10):
    #     for y in range(10):
    #         grid_copy[x][y] = grid[x][y]
    num = 0
    def dfs(row, col):
        if row >= 10 or col >= 10 or row < 0 or col < 0 or grid[row][col] or grid_path[row][col] == 0:
            return
        diff = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        grid_path[row][col] = 0
        for dx, dy in diff:
            dfs(row + dx, col + dy)

    dfs(i, j)
    for x in range(10):
        for y in range(10):
            if grid_path[x][y] == 0:
                num += 1
    return num


if __name__ == '__main__':
    import doctest
    doctest.testmod()
