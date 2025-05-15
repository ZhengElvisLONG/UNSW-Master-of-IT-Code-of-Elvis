# Exercise 1: Diagonal Wave Pattern
# Prints a pattern where numbers increment along diagonals.
# The pattern fills a square grid of size x size.
# Diagonals move from bottom-left to top-right.
#
# Note that NONE OF THE LINES THAT ARE OUTPUT HAS TRAILING SPACES.

def diagonal_wave_pattern(size):
    """
    Prints a diagonal wave pattern of numbers in a square grid.
    Assumes size is a positive integer.
    
    >>> diagonal_wave_pattern(1)
    1
    >>> diagonal_wave_pattern(2)
    1 2
    3 4
    >>> diagonal_wave_pattern(3)
    1 2 4
    3 5 7
    6 8 9
    >>> diagonal_wave_pattern(4)
     1  2  4  7
     3  5  8 11
     6  9 12 14
    10 13 15 16
    >>> diagonal_wave_pattern(5)
     1  2  4  7 11
     3  5  8 12 16
     6  9 13 17 20
    10 14 18 21 23
    15 19 22 24 25
    """
    # if size <= 0:
    #     return
    
    # grid = [[0 for _ in range(size)] for _ in range(size)]
    # num = 1
    # max_len = len(str(size * size))
    
    # # Fill diagonals starting from the first column
    # for k in range(size):
    #     i, j = k, 0
    #     while i >= 0 and j < size:
    #         grid[i][j] = num
    #         num += 1
    #         i -= 1
    #         j += 1
            
    # # Fill diagonals starting from the last row (excluding the first element)
    # for k in range(1, size):
    #     i, j = size - 1, k
    #     while i >= 0 and j < size:
    #         grid[i][j] = num
    #         num += 1
    #         i -= 1
    #         j += 1
            
    # # Print the grid with proper formatting
    # for i in range(size):
    #     row_str = []
    #     for j in range(size):
    #         row_str.append(str(grid[i][j]).rjust(max_len))
    #     print(" ".join(row_str))
    if size < 1:
        return
    matrix = [[0 for _ in range(size)] for _ in range(size)]
    # def fillup(row, col, current):
    #     if 0 <= row < size and 0 <= col < size:
    #         return current
    #     matrix[row][col] = current
    #     current += 1
    #     # print(matrix)
    #     fillup(row + 1, col - 1, current)
    #     return current
    # current = 1
    # for i in range(size):
    #     current = fillup(0, i, current)
    # for i in range(1, size):
    #     current = fillup(i, size - 1, current)
    current = 1
    for cols in range(size):
        col = cols
        row = 0
        while (0 <= row < size and 0 <= col < size):
            matrix[row][col] = current
            current += 1
            row += 1
            col -= 1
    for rows in range(1, size):
        row = rows
        col = size - 1
        while (0 <= row < size and 0 <= col < size):
            matrix[row][col] = current
            current += 1
            row += 1
            col -= 1
    for i in range(size):
        result = " " * (len(str(current - 1)) - len(str(matrix[i][0]))) + str(matrix[i][0])
        for j in range(1, size):
            result += " " * (len(str(current - 1)) - len(str(matrix[i][j])) + 1) + str(matrix[i][j])
        print(result.rstrip())

if __name__ == '__main__':
    import doctest
    doctest.testmod()

