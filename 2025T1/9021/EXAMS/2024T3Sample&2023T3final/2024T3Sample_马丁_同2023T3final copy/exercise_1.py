# Note that NONE OF THE LINES THAT ARE OUTPUT HAS TRAILING SPACES.
#
# You can assume that vertical_bars() is called with nothing but
# integers at least equal to 0 as arguments (if any).


def vertical_bars(*x):
    '''
    >>> vertical_bars()
    >>> vertical_bars(0, 0, 0)
    >>> vertical_bars(4)
    *
    *
    *
    *
    >>> vertical_bars(4, 4, 4)
    * * *
    * * *
    * * *
    * * *
    >>> vertical_bars(4, 0, 3, 1)
    *
    *   *
    *   *
    *   * *
    >>> vertical_bars(0, 1, 2, 3, 2, 1, 0, 0)
          *
        * * *
      * * * * *
    '''
    # 1. 永远先处理空输入
    if not x:
        return
    # 2. 初始化矩阵，注意行和列要反过来
    lst = list(x)
    height, width = max(lst), len(lst) # 行和列反过来，下面第一轮循环要注意，第二轮循环就正常了
    matrix = [[" " for _ in range(height)] for _ in range(width)]
    # 2. 先横打，处理好，倒置好
    for i in range(width):
        for j in range(height):
            if j < lst[i]:
                matrix[i][j] = '*'
        matrix[i].reverse() # 因为从下到上
    # 3. 转置矩阵
    matrix = list(map(list, zip(*matrix))) # 转置矩阵的套路
    for i in range(height):
        # 注意rstrip
        print(" ".join(matrix[i]).rstrip())

if __name__ == '__main__':
    import doctest
    doctest.testmod()
