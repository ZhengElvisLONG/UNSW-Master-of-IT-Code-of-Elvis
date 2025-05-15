# You can assume that the first two arguments to rectangle() are
# integers at least equal to 0, and that the third argument, if any,
# is a string consisting of an uppercase letter.
#
# The rectangle is read by going down the first column (if it exists),
# up the second column (if it exists), down the third column (if it exists),
# up the fourth column  (if it exists)...
#
# Hint: ord() and chr() are useful.

#—————————————————————————————真题真题真题真题真题真题真题真题真题真题真题真题真题真题———————————————————————————————————
# def rectangle(width, height, starting_from='A'):
#     '''
#     >>> rectangle(0, 0)
#     >>> rectangle(10, 1, 'V')
#     VWXYZABCDE
#     >>> rectangle(1, 5, 'X')
#     X
#     Y
#     Z
#     A
#     B
#     >>> rectangle(10, 7)
#     ANOBCPQDER
#     BMPADORCFQ
#     CLQZENSBGP
#     DKRYFMTAHO
#     EJSXGLUZIN
#     FITWHKVYJM
#     GHUVIJWXKL
#     >>> rectangle(12, 4, 'O')
#     OVWDELMTUBCJ
#     PUXCFKNSVADI
#     QTYBGJORWZEH
#     RSZAHIPQXYFG
#     '''
#     result = [["" for _ in range(height)] for _ in range(width)]
#     for i in range(width):
#         for j in range(height):
#             result[i][j] = starting_from
#             starting_from = chr((ord(starting_from) + 1 - ord('A')) % 26 + ord('A'))
#         if i % 2:
#             result[i].reverse()
#     result = list(map(list, zip(*result)))
#     for i in range(height):
#         for j in range(width):
#             print(result[i][j], end = "")
#         print()
        
# if __name__ == '__main__':
#     import doctest
#     doctest.testmod()
# ——————————————————————————————————————————————添加reverse————————————————————————————————————————————————————
# def rectangle(width, height, starting_from='A', reverse = False): #如果reverse为True，从左下角开始打印
#     '''
#     >>> rectangle(0, 0)
#     >>> rectangle(10, 1, 'V')
#     VWXYZABCDE
#     >>> rectangle(1, 5, 'X', True)
#     B
#     A
#     Z
#     Y
#     X
#     >>> rectangle(10, 7)
#     ANOBCPQDER
#     BMPADORCFQ
#     CLQZENSBGP
#     DKRYFMTAHO
#     EJSXGLUZIN
#     FITWHKVYJM
#     GHUVIJWXKL
#     >>> rectangle(12, 4, 'O')
#     OVWDELMTUBCJ
#     PUXCFKNSVADI
#     QTYBGJORWZEH
#     RSZAHIPQXYFG
#     '''
#     result = [["" for _ in range(height)] for _ in range(width)]
#     for i in range(width):
#         for j in range(height):
#             result[i][j] = starting_from
#             starting_from = chr((ord(starting_from) + 1 - ord('A')) % 26 + ord('A'))
#         if (i % 2 and not reverse) or (not i % 2 and reverse):
#             result[i].reverse()
#     result = list(map(list, zip(*result)))
#     for i in range(height):
#         for j in range(width):
#             print(result[i][j], end = "")
#         print()

# if __name__ == '__main__':
#     import doctest
#     doctest.testmod()
# ————————————————————————————————————————————————正横向————————————————————————————————————————————————————————————
# def rectangle(width, height, starting_from='A'):
#     '''
#     >>> rectangle(0, 0)
#     >>> rectangle(10, 1, 'V')
#     VWXYZABCDE
#     >>> rectangle(1, 5, 'X')
#     X
#     Y
#     Z
#     A
#     B
#     >>> rectangle(10, 7)
#     ABCDEFGHIJ
#     KLMNOPQRST
#     UVWXYZABCD
#     EFGHIJKLMN
#     OPQRSTUVWX
#     YZABCDEFGH
#     IJKLMNOPQR
#     >>> rectangle(12, 4, 'O')
#     OPQRSTUVWXYZ
#     ABCDEFGHIJKL
#     MNOPQRSTUVWX
#     YZABCDEFGHIJ
#     '''
#     result = [[] for _ in range(height)]
#     cur_char = starting_from
#     index = 0
#     direction = 1
#     for index in range(height):
#         for i in range(width):
            
#             result[index].append(cur_char)
#             if cur_char == 'Z':
#                 cur_char = 'A'
#             else:
#                 cur_char = chr(ord(cur_char) + 1)
        
#     for line in result:
#         print(''.join(line))

# if __name__ == '__main__':
#     import doctest
#     doctest.testmod()


# ————————————————————————————————————————————————蛇形横向————————————————————————————————————————————————————————————
# def rectangle(width, height, starting_from='A'):
#     '''
#     >>> rectangle(0, 0)
#     >>> rectangle(10, 1, 'V')
#     VWXYZABCDE
#     >>> rectangle(1, 5, 'X')
#     X
#     Y
#     Z
#     A
#     B
#     >>> rectangle(10, 7)
#     ABCDEFGHIJ
#     TSRQPONMLK
#     UVWXYZABCD
#     NMLKJIHGFE
#     OPQRSTUVWX
#     HGFEDCBAZY
#     IJKLMNOPQR
#     >>> rectangle(12, 4, 'O')
#     OPQRSTUVWXYZ
#     LKJIHGFEDCBA
#     MNOPQRSTUVWX
#     JIHGFEDCBAZY
#     '''
#     result = []
#     cur_char = starting_from

#     for row in range(height):
#         line = []
#         for col in range(width):
#             line.append(cur_char)
#             if cur_char == 'Z':
#                 cur_char = 'A'
#             else:
#                 cur_char = chr(ord(cur_char) + 1)

#         if row % 2 == 1:
#             line.reverse()
#         result.append(''.join(line))

#     for line in result:
#         print(line)

# if __name__ == '__main__':
#     import doctest
#     doctest.testmod()


# ———————————————————————————————————————————————————右下左上螺旋———————————————————————————————————————————————————————
# def rectangle(width, height, starting_from='A'):
#     '''
#     >>> rectangle(0, 0)
#     >>> rectangle(1, 1)
#     A
#     >>> rectangle(1, 5)
#     A
#     B
#     C
#     D
#     E
#     >>> rectangle(5, 4, 'X')
#     XYZAB
#     KLMNC
#     JQPOD
#     IHGFE
#     >>> rectangle(7, 5, 'Z')
#     ZABCDEF
#     STUVWXG
#     REFGHYH
#     QDCBAZI
#     PONMLKJ
#     '''
#     result = [[" " for _ in range(width)] for _ in range(height)]
#     top, left, bottom, right = 0, 0, height - 1, width - 1
#     num = 0
#     def next(letter):
#         return chr((ord(letter) + 1 - ord('A')) % 26 + ord('A'))
#     while num < width * height:
#         for i in range(left, right + 1):
#             result[top][i] = starting_from
#             starting_from = next(starting_from)
#             num += 1
#         top += 1
#         if num == width * height:
#             break
#         for i in range(top, bottom + 1):
#             result[i][right] = starting_from
#             starting_from = next(starting_from)
#             num += 1
#         right -= 1
#         if num == width * height:
#             break
#         for i in range(right, left - 1, -1):
#             result[bottom][i] = starting_from
#             starting_from = next(starting_from)
#             num += 1
#         bottom -= 1
#         if num == width * height:
#             break
#         for i in range(bottom, top - 1, -1):
#             result[i][left] = starting_from
#             starting_from = next(starting_from)
#             num += 1
#         left += 1
#         if num == width * height:
#             break
#     for i in range(height):
#         for j in range(width):
#             print(result[i][j], end = "")
#         print()
#     if width == 0 or height == 0:
#         return

#     # 初始化二维矩阵
#     result = [['' for _ in range(width)] for _ in range(height)]

#     # 设置起始字母
#     cur_char = starting_from

#     # 定义四个方向：右、下、左、上
#     dirs = [(0, 1), (1, 0), (0, -1), (-1, 0)]
#     direction = 0  # 初始方向向右
#     x, y = 0, 0    # 初始位置左上角

#     for _ in range(width * height):
#         # 设置当前格的字符
#         result[x][y] = cur_char

#         # 更新下一个字符
#         cur_char = 'A' if cur_char == 'Z' else chr(ord(cur_char) + 1)

#         # 计算下一步坐标
#         nx, ny = x + dirs[direction][0], y + dirs[direction][1]

#         # 判断是否需要转向
#         if 0 <= nx < height and 0 <= ny < width and result[nx][ny] == '':
#             x, y = nx, ny
#         else:
#             # 改变方向
#             direction = (direction + 1) % 4
#             x, y = x + dirs[direction][0], y + dirs[direction][1]

#     # 输出结果
#     for row in result:
#         print(''.join(row))

# if __name__ == '__main__':
#     import doctest
#     doctest.testmod()


# ———————————————————————————————————————————————————左上右下螺旋———————————————————————————————————————————————————————
def rectangle(width, height, starting_from='A'):
    '''
    >>> rectangle(0, 0)
    >>> rectangle(1, 1)
    A
    >>> rectangle(1, 5)
    E
    D
    C
    B
    A
    >>> rectangle(5, 4, 'X')
    EFGHI
    DOPQJ
    CNMLK
    BAZYX
    >>> rectangle(7, 5, 'Z')
    JKLMNOP
    IZABCDQ
    HYHGFER
    GXWVUTS
    FEDCBAZ
    '''
#     if width == 0 or height == 0:
#         return

#     result = [['' for _ in range(width)] for _ in range(height)]

#     cur_char = starting_from

#     # 方向：左 → 上 → 右 → 下（顺时针）
#     dirs = [(0, -1), (-1, 0), (0, 1), (1, 0)]
#     direction = 0  # 初始向左
#     row, col = height - 1, width - 1  # 起始于右下角

#     for _ in range(width * height):
#         result[row][col] = cur_char
#         cur_char = 'A' if cur_char == 'Z' else chr(ord(cur_char) + 1)

#         # 下一步坐标
#         next_row = row + dirs[direction][0]
#         next_col = col + dirs[direction][1]

#         # 判断是否出界或已填过
#         if (0 <= next_row < height and 0 <= next_col < width 
#                 and result[next_row][next_col] == ''):
#             row, col = next_row, next_col
#         else:
#             direction = (direction + 1) % 4
#             row += dirs[direction][0]
#             col += dirs[direction][1]

#     for line in result:
#         print(''.join(line))
    result = [[" " for _ in range(width)] for _ in range(height)]
    top, left, bottom, right = 0, 0, height - 1, width - 1
    num = 0
    def next(letter):
        return chr((ord(letter) + 1 - ord('A')) % 26 + ord('A'))
    while num < width * height:
        for i in range(right, left - 1, -1):
            result[bottom][i] = starting_from
            starting_from = next(starting_from)
            num += 1
        bottom -= 1
        if num == width * height:
            break
        for i in range(bottom, top - 1, -1):
            result[i][left] = starting_from
            starting_from = next(starting_from)
            num += 1
        left += 1
        if num == width * height:
            break
        for i in range(left, right + 1):
            result[top][i] = starting_from
            starting_from = next(starting_from)
            num += 1
        top += 1
        if num == width * height:
            break
        for i in range(top, bottom + 1):
            result[i][right] = starting_from
            starting_from = next(starting_from)
            num += 1
        right -= 1
        if num == width * height:
            break
    for i in range(height):
        for j in range(width):
            print(result[i][j], end = "")
        print()

if __name__ == '__main__':
    import doctest
    doctest.testmod()
