"""
DFS题型方法总结

# 1. 回溯问题
# 需要回溯的情况：
# - 需要探索所有可能路径的问题（如单词搜索、最长递增路径）
# - 需要找到所有解或排列组合的问题
# - 临时标记访问状态的情况
#
# 不需要回溯的情况：
# - 统计连通分量（如岛屿计数、省份问题）
# - 永久性修改输入数据（如洪水填充）
# - 仅需判断存在性的问题（如路径查找）
"""

"""
# 2. 返回值处理
# - 计数问题：无返回值，外部计数器递增（如岛屿计数）
# - 存在判断：返回布尔值，用OR连接各分支（如迷宫寻路）
# - 路径统计：返回数值，用MAX/MIN连接分支（如最长路径、最大路径和）
# - 修改问题：无返回值，直接修改原数据（如洪水填充）
"""

"""
# 3. 访问标记
# 使用visited的场景：
# - 所有图遍历问题（防环）
# - 节点可能被多次访问的情况
#
# 实现方式：
# - 单独visited矩阵（最常用）
# - 修改原网格数据（如把'1'改为'0'）
# - 使用集合记录（适合图节点）
"""

"""
# 4. 终止条件顺序（重要！）
# 必须按以下顺序检查：
# 1. 越界判断
# 2. 已访问判断
# 3. 问题特殊条件（如墙壁、水域等）
# 4. 成功条件（如到达终点、找到单词）
"""

"""
# 5. 计数模式
# - 连通分量：DFS开始前递增计数（如count_islands）
# - 路径数量：返回递归调用的和（多分支累加）
# - 极值路径：返回递归调用的最大/最小值（如max_path_sum）
"""

"""
# 6. 搜索方向
# - 四方向：(dx, dy) = [(0,1),(1,0),(0,-1),(-1,0)]
# - 八方向：包含对角线移动
# - 图邻接：按照邻接表遍历（如course_schedule）
"""

"""
# 7. 特殊问题处理
# - 树问题：通常不需要visited（如max_depth）
# - 环检测：需要"栈中节点"标记（如course_schedule）
# - 记忆化：优化重复计算（如longest_increasing_path）
"""

"""
# 8. 常见错误
# - 忘记在递归前标记visited
# - 终止条件顺序错误
# - 混淆网格和图的表示方式
# - 错误使用回溯（该回溯时没回溯，不该回溯时回溯）
"""


"""
Problem 1: Island Counting

Count the number of islands in a 2D grid. An island is surrounded by water and is formed by connecting adjacent lands horizontally or vertically.
"""

def count_islands(grid):
    """
    Count the number of islands in a 2D grid. An island is surrounded by water and is formed by
    connecting adjacent lands horizontally or vertically.
    
    >>> grid = [
    ...     ['1', '1', '0', '0', '0'],
    ...     ['1', '1', '0', '0', '0'],
    ...     ['0', '0', '1', '0', '0'],
    ...     ['0', '0', '0', '1', '1']
    ... ]
    >>> count_islands(grid)
    3
    """
    # 数岛数的题型：1. 不用回溯，2. 另建一个visited数组或让岛沉没，3. 注意是字符还是数字，容易玩文字游戏
    # 先干掉空值
    if not grid:
        return 0
    # 建立visited
    rows = len(grid)
    cols = len(grid[0])
    visited = [[False for _ in range(cols)] for _ in range(rows)]

    def dfs(row, col):
        # 先写超限或不该访问或已访问
        if row >= rows or col >= cols or col < 0 or row < 0 or grid[row][col] == '0' or visited[row][col]:
            return
        # 设置当前已访问
        # 如果到了终点，这个题不用
        visited[row][col] = True
        # 访问四邻域
        dfs(row, col + 1)
        dfs(row + 1, col)
        dfs(row, col - 1)
        dfs(row - 1, col)
        # 不用回溯
        # visited[row][col] = False

    num = 0
    for i in range(rows):
        for j in range(cols):
            if grid[i][j] == '1' and not visited[i][j]:
                dfs(i, j)
                num += 1
    return num
if __name__ == '__main__':
    import doctest
    doctest.testmod()

"""
Problem 2: Path Finding in a Maze

Determine if there's a path from start to destination in the maze. 0 represents empty space, 1 represents wall.
"""

def has_path(maze, start, destination):
    """
    Determine if there's a path from start to destination in the maze.
    0 represents empty space, 1 represents wall.
    
    >>> maze = [
    ...     [0, 0, 1, 0, 0],
    ...     [0, 0, 0, 0, 0],
    ...     [0, 0, 0, 1, 0],
    ...     [1, 1, 0, 1, 1],
    ...     [0, 0, 0, 0, 0]
    ... ]
    >>> start = (0, 0)
    >>> destination = (4, 4)
    >>> has_path(maze, start, destination)
    True
    """
    # 是否有路径问题：1. 要设置visited，2. return的是是否，不用回溯
    # 先干掉空值
    if not maze:
        return False
    rows, cols = len(maze), len(maze[0])
    visited = [[False for _ in range(cols)] for _ in range(rows)]
    # 因为只返回是否，不用记录路径
    def dfs(x, y):
        # 如果越界和遇墙或已走过
        if x < 0 or y < 0 or x >= rows or y >= cols or maze[x][y] == 1 or visited[x][y]:
            return False
        # 如果到达
        if (x, y) == destination:
            return True
        # 先走过当前，再向四邻域递归，如果有成功就成功
        visited[x][y] = True
        if dfs(x + 1, y) or dfs(x - 1, y) or dfs(x, y - 1) or dfs(x, y + 1):
            return True
    return dfs(start[0], start[1])

if __name__ == '__main__':
    import doctest
    doctest.testmod()

"""
Problem 3: Maximum Depth of Binary Tree

Find the maximum depth of a binary tree.
"""

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def max_depth(root):
    """
    Find the maximum depth of a binary tree.
    
    >>> root = TreeNode(3, TreeNode(9), TreeNode(20, TreeNode(15), TreeNode(7)))
    >>> max_depth(root)
    3
    """
    def dfs(root):
        if not root:
            return 0
        return max(dfs(root.left), dfs(root.right)) + 1
    return dfs(root)

"""
Problem 4: Number of Provinces

Find the number of provinces in a graph represented by an adjacency matrix. A province is a group of directly or indirectly connected cities.
"""

def find_provinces(isConnected):
    """
    Find the number of provinces in a graph represented by an adjacency matrix.
    A province is a group of directly or indirectly connected cities.
    
    >>> isConnected = [[1,1,0],[1,1,0],[0,0,1]]
    >>> find_provinces(isConnected)
    2
    """
    if not isConnected:
        return 0
    rows = len(isConnected)
    cols = len(isConnected[0])
    visited = [[False for _ in range(cols)] for _ in range(rows)]
    def dfs(x, y):
        if x < 0 or y < 0 or x >= cols or y >= rows or not isConnected[x][y] or visited[x][y]:
            return
        visited[x][y] = True
        dfs(x + 1, y)
        dfs(x - 1, y)
        dfs(x, y + 1)
        dfs(x, y - 1)
    num = 0
    for i in range(rows):
        for j in range(cols):
            if not visited[i][j] and isConnected[i][j]:
                dfs(i, j)
                num += 1
    return num

"""
Problem 5: Word Search

Determine if the word can be found in the board by connecting adjacent cells.
"""

def exist(board, word):
    """
    Determine if the word can be found in the board by connecting adjacent cells.
    
    >>> board = [
    ...     ['A','B','C','S'],
    ...     ['S','F','C','E'],
    ...     ['A','D','E','E']
    ... ]
    >>> exist(board, "ABCCED")
    True
    >>> exist(board, "SEE")
    True
    >>> exist(board, "ABCB")
    False
    """
    # 去掉空列表
    if not board:
        return False
    rows = len(board)
    cols = len(board[0])
    visited = [[False for _ in range(cols)] for _ in range(rows)]
    def dfs(x, y, lst):
        # 越界、不匹配或已走过
        if x >= rows or y >= cols or x < 0 or y < 0 or visited[x][y] or board[x][y] != lst[0]:
            return False
        # 如果最前一位匹配，标记已走过，继续看后面几位直到结束
        visited[x][y] = True
        if len(lst) == 1:
            return True
        rst = dfs(x + 1, y, lst[1:]) or dfs(x - 1, y, lst[1:]) or dfs(x, y - 1, lst[1:]) or dfs(x, y + 1, lst[1:])
        visited[x][y] = False
        return rst
    result = False
    for i in range(rows):
        for j in range(cols):
            result = dfs(i, j, word)
            if result == True:
                return result
    return result

"""
Problem 6: Flood Fill

Perform a flood fill on the image starting at (sr, sc).
"""

def flood_fill(image, sr, sc, new_color):
    """
    Perform a flood fill on the image starting at (sr, sc).
    
    >>> image = [
    ...     [1,1,1],
    ...     [1,1,0],
    ...     [1,0,1]
    ... ]
    >>> flood_fill(image, 1, 1, 2)
    [[2, 2, 2], [2, 2, 0], [2, 0, 1]]
    >>> image = [
    ...     [1,1,1],
    ...     [1,1,0],
    ...     [1,0,1]
    ... ]
    >>> flood_fill(image, 2, 2, 2)
    [[1, 1, 1], [1, 1, 0], [1, 0, 2]]
    """
    rows = len(image)
    cols = len(image[0])
    visited = [[False for _ in range(cols)] for _ in range(rows)]
    def dfs(x, y):
        # 如果越界、已访问或不是1
        if x >= rows or x < 0 or y >= cols or y < 0 or image[x][y] == 0 or visited[x][y]:
            return
        # 标记已访问，递归四邻域
        visited[x][y] = True
        dfs(x + 1, y)
        dfs(x - 1, y)
        dfs(x, y - 1)
        dfs(x, y + 1)
    dfs(sr, sc)
    for i in range(rows):
        for j in range(cols):
            if visited[i][j]:
                image[i][j] = new_color
    print(image)

"""
Problem 7: Course Schedule

Determine if it's possible to finish all courses given prerequisites.
"""

def can_finish(num_courses, prerequisites):
    """
    Determine if it's possible to finish all courses given prerequisites.
    
    >>> can_finish(2, [[1,0]])
    True
    >>> can_finish(2, [[1,0], [0,1]])
    False
    """
    # 环检测题型，设visited、has_cycle两个bool列表存储，如果一个栈有点被重复访问就是有栈上所有节点都有环，需要回溯
    has_cycle = [False for _ in range(num_courses)]
    visited = [False for _ in range(num_courses)]
    def dfs(current):
        # 越界/不能走
        # 如果一个节点两次被访问
        if visited[current]:
            has_cycle[current] = True  # 发现环
            return
        # 访问当前
        visited[current] = True
        for item in prerequisites:
            if item[0] == current:
                # 递归
                dfs(item[1])
                # 如果子节点有环，当前节点也有环
                if has_cycle[current]:
                    return
        visited[current] = False  # 回溯

    for i in range(num_courses):
        if not visited[i]:
            dfs(i)
    for i in range(num_courses):
        if has_cycle[i]:
            return False
    return True

"""
Problem 8: Maximum Value Path in a Grid

Find the path with the maximum sum in a grid, moving only right or down.
"""

def find_max_path(grid):
    """
    Find the path with the maximum sum in a grid, moving only right or down.
    
    >>> grid = [
    ...     [1, 3, 1],
    ...     [1, 5, 1],
    ...     [4, 2, 1]
    ... ]
    >>> find_max_path(grid)
    12
    """
    # 路径最大和问题
    if not grid:
        return 0
    rows = len(grid)
    cols = len(grid[0])
    def dfs(curr_sum, x, y):
        # 超限
        if x >= rows or x < 0 or y >= cols or y < 0:
            return 0
        # 访问当前
        curr_sum += grid[x][y]
        # 到达终点
        if x == rows - 1 and y == cols - 1:
            return curr_sum
        # 同二叉树深度
        return max(dfs(curr_sum, x + 1, y), dfs(curr_sum, x, y + 1))
    return dfs(0, 0, 0)

"""
Problem 9: Keys and Rooms

Determine if you can visit all rooms by collecting keys.
"""

def can_visit_all_rooms(rooms):
    """
    Determine if you can visit all rooms by collecting keys.
    
    >>> rooms = [[1], [2], [3], []]
    >>> can_visit_all_rooms(rooms)
    True
    >>> rooms = [[1,3], [3,0,1], [2], [0]]
    >>> can_visit_all_rooms(rooms)
    False
    """
    # 只要求遍历
    can_visit = [False] * len(rooms)
    visited = [False] * len(rooms)
    def dfs(current):
        # 走过当前
        visited[current] = True
        # 递归走过当前增加且没走过的
        for item in rooms[current]:
            can_visit[item] = True
            if not visited[item]:
                dfs(item)
        # 能走的都走过了
        if can_visit == visited:
            return
    dfs(0)
    for i in visited:
        if not i:
            return False
    return True

"""
Problem 10: Longest Increasing Path in a Matrix

Find the length of the longest increasing path in a matrix.
"""

def longest_increasing_path(matrix):
    """
    Find the length of the longest increasing path in a matrix.
    
    >>> matrix = [
    ...     [9, 9, 4],
    ...     [6, 6, 8],
    ...     [2, 1, 1]
    ... ]
    >>> longest_increasing_path(matrix)
    4
    """
    # 路径计数型：1. 需要回溯，2. 返回邻域内最大的次数，3. 每个点dfs取最大
    if not matrix:
        return 0
    rows = len(matrix)
    cols = len(matrix[0])
    visited = [[False for _ in range(cols)] for _ in range(rows)]
    def dfs(x, y, time):
        # 超限
        if x < 0 or y < 0 or x >= rows or y >= cols or visited[x][y]:
            return time
        # 走过当前
        visited[x][y] = True
        diff = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        rst = []
        max_time = time
        # 递归找四邻域的最大time
        for dx, dy in diff:
            nx, ny = x + dx, y + dy
            if 0 <= nx < rows and 0 <= ny < cols and matrix[nx][ny] > matrix[x][y]:
                current_time = dfs(nx, ny, time + 1)
                if current_time > max_time:
                    max_time = current_time
        # 回溯
        visited[x][y] = False
        return max_time
    mtime = 0
    for i in range(rows):
        for j in range(cols):
            # 开头是time = 1，不是0
            if mtime < dfs(i, j, 1):
                mtime = dfs(i, j, 1)
    return mtime

"""
Problem 11: Explore from (Original Problem)

Implement the `explore_from` function for a grid traversal problem.
"""

def explore_from(grid, upper_bound, i, j):
    """
    Explore the grid starting from position (i, j) and find the maximum value
    that can be reached by traveling through consecutive increasing numbers.
    
    Travelling from m to n means starting from a cell that stores m,
    moving to a (horizontally, vertically or diagonally) neighbouring
    cell that stores m + 1, then moving to a (horizontally, vertically
    or diagonally) neighbouring cell that stores m + 2... and eventually
    reaching a cell that stores n.
    
    Args:
        grid: A 2D grid with values or '*' for borders
        upper_bound: The maximum possible value in the grid
        i, j: Starting position coordinates
        
    Returns:
        The maximum value that can be reached from grid[i][j]
    """
    # 超限
    if grid[i][j] == "*":
        return 0
    current = grid[i][j]
    max_num = current
    # 到达上限
    if current == upper_bound:
        return upper_bound
    # 递归搜索八邻域
    diffs = [(0, 1), (0, -1), (1, 0), (1, 1), (1, -1), (-1, 0), (-1, 1), (-1, -1)]
    for dx, dy in diffs:
        ni, nj = i + dx, j + dy
        # 判断能不能走
        if grid[ni][nj] == current + 1:
            found = explore_from(grid, upper_bound, ni, nj)
            if found > max_num:
                max_num = found
                # 重复：如果到达上限，结束
                if max_num == upper_bound:
                    return max_num
    return max_num