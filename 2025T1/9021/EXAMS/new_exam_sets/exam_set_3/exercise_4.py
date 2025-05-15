# Exercise 4: Number Spiral in Rectangle
# Creates a spiral pattern using consecutive numbers starting from 1.
# The spiral starts from the top-left corner and moves clockwise inwards.
# The pattern fills a rectangle of size width x height.
# Numbers should be formatted to align nicely based on the maximum number.
#
# You can assume width and height are integers >= 0.
# Note that NONE OF THE LINES THAT ARE OUTPUT HAS TRAILING SPACES.

def number_spiral_rectangle(width, height):
    """
    Creates a clockwise spiral pattern of numbers in a rectangle.
    
    >>> number_spiral_rectangle(0, 0)
    >>> number_spiral_rectangle(1, 1)
    1
    >>> number_spiral_rectangle(3, 1)
    1 2 3
    >>> number_spiral_rectangle(1, 4)
    1
    2
    3
    4
    >>> number_spiral_rectangle(3, 3)
     1  2  3
     8  9  4
     7  6  5
    >>> number_spiral_rectangle(4, 3)
     1  2  3  4
    10 11 12  5
     9  8  7  6
    >>> number_spiral_rectangle(5, 4)
     1  2  3  4  5
    14 15 16 17  6
    13 20 19 18  7
    12 11 10  9  8
    >>> number_spiral_rectangle(6, 5)
     1  2  3  4  5  6
    20 21 22 23 24  7
    19 28 29 30 25  8
    18 27 26 15 14  9
    17 16 11 10 13 12
    """
    # if width <= 0 or height <= 0:
    #     return

    # total_cells = width * height
    # max_num_len = len(str(total_cells))
    # grid = [[0 for _ in range(width)] for _ in range(height)]
    # top, bottom, left, right = 0, height - 1, 0, width - 1
    # direction = 0  # 0: right, 1: down, 2: left, 3: up
    # num = 1

    # while top <= bottom and left <= right:
    #     if direction == 0:  # Move right
    #         for i in range(left, right + 1):
    #             grid[top][i] = num
    #             num += 1
    #         top += 1
    #     elif direction == 1:  # Move down
    #         for i in range(top, bottom + 1):
    #             grid[i][right] = num
    #             num += 1
    #         right -= 1
    #     elif direction == 2:  # Move left
    #         for i in range(right, left - 1, -1):
    #             grid[bottom][i] = num
    #             num += 1
    #         bottom -= 1
    #     elif direction == 3:  # Move up
    #         for i in range(bottom, top - 1, -1):
    #             grid[i][left] = num
    #             num += 1
    #         left += 1
        
    #     direction = (direction + 1) % 4

    # # Print the grid with formatting
    # for row in grid:
    #     row_str = [str(n).rjust(max_num_len) if n != 0 else " " * max_num_len for n in row]
    #     print(" ".join(row_str))
    if height == 0 or width == 0:
        return
    top, bottom, left, right = 0, height - 1, 0, width - 1
    result = [[0 for _ in range(width)] for _ in range(height)]
    current = 1
    while current <= width * height:
        for i in range(left, right + 1):
            result[top][i] = current
            current += 1
        top += 1
        if current > width * height:
            break
        for j in range(top, bottom + 1):
            result[j][right] = current
            current += 1
        right -= 1
        if current > width * height:
            break
        for i in range(right, left - 1, -1):
            result[bottom][i] = current
            current += 1
        bottom -= 1
        if current > width * height:
            break
        for j in range(bottom, top - 1, -1):
            result[j][left] = current
            current += 1
        left += 1
        if current > width * height:
            break
    current -= 1
    # for i in range(height):
    #     result = " " * (len(str(current)) - len(str(result[i][0]))) + str(result[i][0])
    #     for j in range(1, width):
    #         result += " " * (len(str(current)) - len(str(result[i][j]))) + str(result[i][j])
    #     print(result)
    max_digits = len(str(current)) if current > 0 else 1  # 最大数字的位数
    for row in result:
        formatted_row = []
        for num in row:
            # 每个数字右对齐，宽度为 max_digits
            formatted_num = f"{num:>{max_digits}}"
            formatted_row.append(formatted_num)
        print(" ".join(formatted_row).rstrip())  # 用空格连接同一行的数字

if __name__ == '__main__':
    import doctest
    doctest.testmod()

