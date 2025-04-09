# Written by Zheng LONG for COMP9021
#
# Implements a function display_leftmost_topmost_boundary(*grid)
# whose argument grid is supposed to be a sequence of strings
# all of the same length, consisting of nothing but spaces and *s,
# that represent one or more "full polygons" that do not "touch"
# each other.
# The selected polygon's top boundary is as high as possible ,
# and amongst all polygons whose top boundary is as high as possible,
# the selected polygon's top boundary starts as much to the left
# as possible.
# Each line of the output has the same number of characters,
# that of each string passed as argument.
import numpy as np

def display(*grid):
    for row in grid:
        spaced_row = " ".join(row) # 在每个字符之间插入一个空格
        print(spaced_row)

def neighbours(point, height, width):
    """
    获取指定点的8个邻居坐标，neibours要用八连通
    """
    i, j = point
    offsets = [(-1,0), (-1,1), (0,1), (1,1), (1,0), (1,-1), (0,-1), (-1,-1)]
    return list((i+di, j+dj) for di,dj in offsets if 0 <= i+di < height and 0 <= j+dj < width)

def is_boundary_point(grid, i, j, height, width):
    """
    检查网格中的指定点是否为边界点
    边界点定义为：其4连通邻域（上下左右）中至少有一个点是空白或超出网格范围
    """
    return any(
        (ni < 0 or ni >= height or nj < 0 or nj >= width or grid[ni][nj] == 0)
        for di, dj in [(0, 1), (1, 0), (0, -1), (-1, 0)]
        for ni, nj in [(i + di, j + dj)]
    )

def find_top_left_polygon(polygons):
    """找到最上最左的多边形"""
    # 1. 找到所有多边形中最小的行号（最上边）
    topmost_row = min(p[0] for polygon in polygons for p in polygon)
    
    # 2. 筛选出包含这个最上边的多边形
    candidates = [
        polygon for polygon in polygons 
        if any(p[0] == topmost_row for p in polygon)
    ]
    
    # 3. 在这些候选多边形中找到最左边的点
    leftmost_col = min(p[1] for polygon in candidates for p in polygon if p[0] == topmost_row)
    
    # 4. 选择包含这个最上最左点的多边形
    for polygon in candidates:
        if (topmost_row, leftmost_col) in polygon:
            return polygon
    return set()

def find_all_polygons(grid, height, width):
    """查找网格中的所有多边形"""
    visited = set()
    polygons = []
    
    for i in range(height):
        for j in range(width):
            if grid[i][j] == 1 and (i, j) not in visited:
                # 使用BFS查找连通区域
                queue = [(i, j)]
                current_polygon = set()
                
                while queue:
                    # 从队列中取出一个点
                    x, y = queue.pop(0)
                    # 检查是否已经访问过这个点
                    if (x, y) in visited:
                        continue
                    # 标记为已访问
                    visited.add((x, y))
                    current_polygon.add((x, y))
                    # 遍历所有邻居
                    for ni, nj in neighbours((x, y), height, width):
                        if grid[ni][nj] == 1 and (ni, nj) not in visited:
                            queue.append((ni, nj))
                
                polygons.append(current_polygon)
    
    return polygons

def display_leftmost_topmost_boundary(*grid):
    """
    显示最上最左多边形的边界
    
    参数:
        grid: 包含多行字符串的元组，表示输入的字符网格
    """
    # 检查所有字符串长度是否相同
    # if len(set(len(row) for row in grid)) != 1:
    #     raise ValueError("All strings must be of the same length")
    
    # 获取网格的尺寸
    height = len(grid)
    width = 0 if height == 0 else len(grid[0]) # 获取第一行的长度，防止空网格
    
    # 将字符网格转换为数值网格，便于处理
    graph_in = []
    for row in grid:
        row_values = []
        for char in row:
            row_values.append(0 if char == ' ' else 1)
        graph_in.append(row_values)

    # 找到所有多边形
    polygons = []
    visited = set()
    # 遍历整个网格寻找多边形
    polygons = find_all_polygons(graph_in, height, width)

    # 如果没有找到多边形，直接显示原网格并返回
    if not polygons:
        display(*grid)
        return
    
    # 找到最上最左的多边形
    selected_polygon = find_top_left_polygon(polygons)

    # 如果没有找到多边形，直接显示原网格并返回
    if not selected_polygon:
        display(*grid)
        return
    
    # 创建一个新的网格，用于存储边界点
    graph_boundary = [[0] * width for _ in range(height)]
    # 将选定多边形的所有点标记为1
    for i, j in selected_polygon:
        if is_boundary_point(graph_in, i, j, height, width):
            graph_boundary[i][j] = 1

    # 将数值网格转换回字符网格
    re_dic = {0: ' ', 1: '*'}
    grid_out = []
    for i in range(height):
        row = []
        for j in range(width):
            row.append(re_dic[graph_boundary[i][j]])
        grid_out.append(''.join(row))
    
    # 显示边界网格
    display(*grid_out)

# # 测试用例
# grid_1 = (
#     '  *   ',
#     ' **** ',
#     '***** ',
#     '******',
#     ' **** ',
#     '  **  '
# )
# grid_2 = (' *       ',
#  '***   ** ',
#  ' *** *** ',
#  ' ***  *  ',
#  '****     ',
#  ' **      '
#  )
# # 显示原始网格
# display(*grid_2)
# print("Boundary:")
# # 显示最上最左多边形的边界
# display_leftmost_topmost_boundary(*grid_2)