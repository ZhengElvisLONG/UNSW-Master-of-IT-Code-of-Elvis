# Written by *** for COMP9021
#
# Defines a function meant to take two integers x and y
# at least equal to 0 and having the same number of digits as arguments;
# x and y are to be read as the x and y coordinates of points, respectively.
# For instance, if x is 3040 and y is 2121, then the points are
# (3, 2), (0, 1) and (4, 2) (the point (0, 1) is duplicated).
# Consider that x coordinates increase from left to right
# and y coordinates increase from bottom to top.
#
# The function prints out the list of points in the order they are found
# by scanning the plane row by row, from top to bottom,
# and for a given row from left to right.
#
# The function displays the points as stars,
# with no trailing space on any line,
# except for the "origin", displayed as o,
# defining the "origin" as the leftmost lowest point.
#
# Finally, the function prints out the slopes of the lines
# that go through the "origin" and any other point,
# ordered from smallest to largest.
# When the line is horizontal, the slope is 0/1.
# When the line is vertical, the slope is inf/1
# (note that Python offers float('inf')).
# Consecutive slopes are separated by a comma and a space.
# When there is no slope, an empty line is output.


from math import gcd

def slopes(x, y):
    # 将 x 和 y 转换为字符串，方便逐位处理
    x_str = str(x)
    y_str = str(y)
    
    # 生成点列表
    points = list(set((int(x_str[i]), int(y_str[i])) for i in range(len(x_str))))
    points.sort(key=lambda p: (-p[1], p[0]))
    
    # 打印点列表
    print("Here is the list of points:")
    print(points)
    print()
    
    # 找到原点（最左下方的最低点）
    origin = min(points, key=lambda p: (p[1], p[0]))
    
    # 构建平面，找到 x 和 y 的最小值和最大值
    x_coords = [p[0] for p in points]
    y_coords = [p[1] for p in points]
    xmin, xmax = min(x_coords), max(x_coords)
    ymin, ymax = min(y_coords), max(y_coords)
    
    # 找到原点（最左下方的最低点）
    origin = min(points, key=lambda p: (p[1], p[0]))
    
    # 初始化平面
    plane = [[' ' for _ in range(xmax - xmin + 1)] for _ in range(ymax - ymin + 1)]
    
    # 填充平面
    for p in points:
        x = p[0] - xmin
        y = p[1] - ymin
        if p == origin:
            plane[y][x] = 'o'
        else:
            plane[y][x] = '*'
    
    # 打印平面图
    print("Here they are on the plane:")
    
    # 打印 y 轴和平面内容
    for y_coord in range(ymax, ymin - 1, -1):
        # 打印 y 坐标
        print(f"{y_coord}", end="")
        row_content = []
        for x_coord in range(xmin, xmax + 1):
            x = x_coord - xmin
            y = y_coord - ymin
            row_content.append(plane[y][x])
        # 去掉行尾的空格
        if any(c != ' ' for c in row_content):  # 如果当前行有点
            print(" " + " ".join(row_content).rstrip())
        else:  # 如果当前行没有点
            print()
        
    
    # 打印 x 轴
    print("  ", end="")
    for x_coord in range(xmin, xmax + 1):
        print(x_coord, end="")
        if x_coord != xmax:  # 如果不是最后一个元素，添加空格
            print(" ", end="")
    print()
    print()
    # 计算斜率
    slopes = []
    for p in points:
        if p != origin:
            dx = p[0] - origin[0]
            dy = p[1] - origin[1]
            if dx == 0:
                slopes.append("inf/1")
            elif dy == 0:
                slopes.append("0/1")
            else:
                # 化简斜率
                common_divisor = gcd(dy, dx)
                if dy * dx >= 0:
                    slope = f"{abs(dy) // common_divisor}/{abs(dx) // common_divisor}"
                else:
                    slope = f"{-abs(dy) // common_divisor}/{abs(dx) // common_divisor}"
                slopes.append(slope)
    
    # 按斜率从小到大排序
    slopes = list(set(slopes))
    slopes.sort(key=lambda s: float(s.split('/')[0]) / float(s.split('/')[1]) if '/' in s else float('inf'))

    # 打印斜率
    print("Ordered from smallest to largest, the slopes are:")
    print(", ".join(slopes) if slopes else "")