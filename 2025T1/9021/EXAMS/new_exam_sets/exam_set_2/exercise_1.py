# Exercise 1: Hollow Number Square
# Prints a hollow square pattern using numbers.
# The size parameter determines the dimension of the square.
# The outer frame uses '1', the next inner frame uses '2', and so on.
# The center element (for odd size) or center 2x2 block (for even size)
# will use the highest number.
#
# Note that NONE OF THE LINES THAT ARE OUTPUT HAS TRAILING SPACES.

def hollow_number_square(size):
    """
    Prints a hollow square pattern with incrementing numbers for inner frames.
    Assumes size is a positive integer.
    
    >>> hollow_number_square(1)
    1
    >>> hollow_number_square(2)
    11
    11
    >>> hollow_number_square(3)
    111
    121
    111
    >>> hollow_number_square(4)
    1111
    1221
    1221
    1111
    >>> hollow_number_square(5)
    11111
    12221
    12321
    12221
    11111
    >>> hollow_number_square(6)
    111111
    122221
    123321
    123321
    122221
    111111
    >>> hollow_number_square(7)
    1111111
    1222221
    1233321
    1234321
    1233321
    1222221
    1111111
    """
    # times = (size + 1) // 2
    # result = [[0 for _ in range(size)] for _ in range(size)]
    # top, bottom = 0, size - 1
    # for time in range(1, times + 1):
    #     for i in range(top, bottom + 1):
    #         result[top][i] = time
    #         result[bottom][i] = time
    #         result[i][top] = time
    #         result[i][bottom] = time
    #     top, bottom = top + 1, bottom - 1
    # output = ""
    # for i in range(size):
    #     for j in range(size):
    #         print(result[i][j], end = "")
    #     print()
    if size < 1:
        return
    max_num = (size + 1) // 2
    matrix = [[0 for _ in range(size)] for _ in range(size)]
    top, bottom = 0, size - 1
    for i in range(1, size + 1):
        for j in range(top, bottom + 1):
            matrix[top][j] = i
            matrix[bottom][j] = i
            matrix[j][top] = i
            matrix[j][bottom] = i
        top, bottom = top + 1, bottom - 1
    for i in range(size):
        for j in range(size):
            print(matrix[i][j], end = "")
        print()
        
if __name__ == '__main__':
    import doctest
    doctest.testmod()

