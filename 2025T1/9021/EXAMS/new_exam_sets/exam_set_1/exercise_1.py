# Exercise 1: Centered Number Pyramid
# Prints a centered pyramid of numbers.
# The height determines the maximum number reached at the center.
# Each row contains numbers increasing to the row number and then decreasing.
# Ensure proper centering based on the width of the last row.
#
# Note that NONE OF THE LINES THAT ARE OUTPUT HAS TRAILING SPACES.

def centered_number_pyramid(height):
    """
    Prints a centered number pyramid.
    Assumes height is a positive integer.
    
    >>> centered_number_pyramid(1)
    1
    >>> centered_number_pyramid(2)
     1
    121
    >>> centered_number_pyramid(3)
      1
     121
    12321
    >>> centered_number_pyramid(4)
       1
      121
     12321
    1234321
    >>> centered_number_pyramid(5)
        1
       121
      12321
     1234321
    123454321
    """
    # if height <= 0:
    #     return
    # max_width = len("".join(map(str, list(range(1, height + 1)) + list(range(height - 1, 0, -1)))))
    # for i in range(1, height + 1):
    #     row_nums = list(range(1, i + 1)) + list(range(i - 1, 0, -1))
    #     row_str = "".join(map(str, row_nums))
    #     print(row_str.center(max_width))
    result = ["" for _ in range(height)]
    for n in range(height):
        result[n] += " " * (height- 1 - n)
        for i in range(n + 1):
            result[n] += str(i + 1)
        for i in range(n):
            result[n] += str(n - i)
    for i in range(height):
        print(result[i])

if __name__ == '__main__':
    import doctest
    doctest.testmod()

