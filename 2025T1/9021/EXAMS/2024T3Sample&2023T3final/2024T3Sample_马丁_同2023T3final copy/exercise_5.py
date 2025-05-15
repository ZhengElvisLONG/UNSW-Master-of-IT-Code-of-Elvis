# You can assume that paths() is called with an integer as first
# argument, an integer at least equal to 1 as second argument,
# and integers between 0 and 9 as third and fourth arguments.
#
# A path connects numbers to numbers by moving South,
# South West or South East.
#
# Note that <BLANKLINE> is not output by the program, but
# doctest's way to refer to an empty line
# (here, output by the print() statement in the stub).


from random import seed, randrange
dim = 10


def display(grid):
    print('   ', '-' * (2 * dim + 1))
    for i in range(dim):
        print('   |', ' '.join(str(j) if grid[i][j] else ' '
                                   for j in range(dim)
                              ), end=' |\n'
             )
    print('   ', '-' * (2 * dim + 1))


def paths(for_seed, density, top, bottom):
    '''
    >>> paths(0, 2, 0, 0)
    Here is the grid that has been generated:
        ---------------------
       | 0 1   3 4 5 6 7 8   |
       |   1     4   6     9 |
       | 0   2 3 4   6 7 8   |
       |     2   4 5   7     |
       |       3     6 7   9 |
       | 0   2   4 5   7 8   |
       | 0         5 6       |
       |       3 4     7 8 9 |
       | 0 1   3   5 6       |
       | 0     3   5 6       |
        ---------------------
    <BLANKLINE>
    Here are all paths from 0 at the top to 0 at the bottom:
        ---------------------
       |                     |
       |                     |
       |                     |
       |                     |
       |                     |
       |                     |
       |                     |
       |                     |
       |                     |
       |                     |
        ---------------------
    >>> paths(0, 4, 6, 7)
    Here is the grid that has been generated:
        ---------------------
       | 0 1   3 4 5 6 7 8 9 |
       | 0 1 2   4 5 6     9 |
       | 0   2 3 4 5 6 7 8   |
       |     2   4 5 6 7   9 |
       | 0 1 2 3     6 7   9 |
       | 0   2 3 4 5   7 8 9 |
       | 0 1 2 3   5 6     9 |
       | 0     3 4 5 6 7 8 9 |
       | 0 1   3   5 6 7 8   |
       | 0   2 3 4 5 6     9 |
        ---------------------
    <BLANKLINE>
    Here are all paths from 6 at the top to 7 at the bottom:
        ---------------------
       |                     |
       |                     |
       |                     |
       |                     |
       |                     |
       |                     |
       |                     |
       |                     |
       |                     |
       |                     |
        ---------------------
    >>> paths(0, 4, 6, 6)
    Here is the grid that has been generated:
        ---------------------
       | 0 1   3 4 5 6 7 8 9 |
       | 0 1 2   4 5 6     9 |
       | 0   2 3 4 5 6 7 8   |
       |     2   4 5 6 7   9 |
       | 0 1 2 3     6 7   9 |
       | 0   2 3 4 5   7 8 9 |
       | 0 1 2 3   5 6     9 |
       | 0     3 4 5 6 7 8 9 |
       | 0 1   3   5 6 7 8   |
       | 0   2 3 4 5 6     9 |
        ---------------------
    <BLANKLINE>
    Here are all paths from 6 at the top to 6 at the bottom:
        ---------------------
       |             6       |
       |           5 6       |
       |         4 5 6 7     |
       |         4 5 6 7     |
       |       3     6 7     |
       |     2 3 4 5   7 8   |
       |       3   5 6     9 |
       |         4 5 6 7 8   |
       |           5 6 7     |
       |             6       |
        ---------------------
    >>> paths(0, 4, 0, 2)
    Here is the grid that has been generated:
        ---------------------
       | 0 1   3 4 5 6 7 8 9 |
       | 0 1 2   4 5 6     9 |
       | 0   2 3 4 5 6 7 8   |
       |     2   4 5 6 7   9 |
       | 0 1 2 3     6 7   9 |
       | 0   2 3 4 5   7 8 9 |
       | 0 1 2 3   5 6     9 |
       | 0     3 4 5 6 7 8 9 |
       | 0 1   3   5 6 7 8   |
       | 0   2 3 4 5 6     9 |
        ---------------------
    <BLANKLINE>
    Here are all paths from 0 at the top to 2 at the bottom:
        ---------------------
       | 0                   |
       |   1                 |
       |     2               |
       |     2               |
       |   1 2 3             |
       | 0   2 3 4           |
       | 0 1 2 3   5         |
       | 0     3 4           |
       |   1   3             |
       |     2               |
        ---------------------
    '''
    seed(for_seed)
    grid = [[int(randrange(density) != 0) for _ in range(dim)]
                 for _ in range(dim)
           ]
    print('Here is the grid that has been generated:')
    display(grid)

    # path_grid临时存储，跟visited一样，path存储路径的集合
    path_grid = [[0 for _ in range(dim)] for _ in range(dim)]
    path = [[0 for _ in range(dim)] for _ in range(dim)]

    def dfs(row, col):
        # 1. 边界检查，不能走，已访问
        if row >= dim or row < 0 or col >= dim or col < 0 or not grid[row][col]:
            return
        # 2. 检查是否到达终点
        if row == dim - 1 and col == bottom:
            # 走过当前
            path_grid[row][col] = 1
            # 把临时路径赋予存储
            for i in range(dim):
                for j in range(dim):
                    if path_grid[i][j] - path[i][j] == 1:
                        path[i][j] = 1
            return
        # 3. 走过当前
        path_grid[row][col] = 1
        # 4. 尝试三个可能的方向
        if (dfs(row + 1, col) or
            dfs(row + 1, col - 1) or
            dfs(row + 1, col + 1)):
            return
        # 5. 回溯
        path_grid[row][col] = 0
        return
    dfs(0, top)
    print(f"Here are all paths from {top} at the top to {bottom} at the bottom:")
    display(path)

if __name__ == '__main__':
    import doctest
    doctest.testmod()
