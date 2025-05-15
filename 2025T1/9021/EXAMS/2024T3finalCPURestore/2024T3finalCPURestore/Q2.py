# NO line has any trailing space.

# You can assue that the first argument to f() is an intetger at least
# equal to 2 and the second argument to f() is a nonempty string.

# The output is printes out, not retuened.

from itertools import cycle

#先存储后打印 [[]]
def f(size=2, characters="."):
    '''
    >>> f()
    . .
     .
     .
    . .
    >>> f(3, '+-')
    + - +
     - +
      -
      +
     - +
    - + -
    >>> f(4, '12345')
    1 2 3 4
     5 1 2
      3 4
       5
       1
      2 3
     4 5 1
    2 3 4 5
    >>> f(7, 'A#B')
    A # B A # B A
     # B A # B A
      # B A # B
       A # B A
        # B A
         # B
          A
          #
         B A
        # B A
       # B A #
      B A # B A
     # B A # B A
    # B A # B A #
    '''
    time = 0
    cycle = len(characters)
    current = characters[time % cycle] # 应对越界
    result = ["" for _ in range(2 * size)]
    # 1. 计算好金字塔的前置空格
    for i in range(size):
        result[i] += " " * i
        result[i + size] += " " * (size - i - 1)
    # 2. 填充字符
    for i in range(size):
        for _ in range(size - i, 0, -1): # 要倒序
            result[i] += current + " " # 空格在前面
            time += 1
            current = characters[time % cycle]
    for i in range(size): # 一定要另开一个循环，不能在老循环里做，因为会影响current
        for _ in range(i + 1):
            result[i + size] += current + " "
            time += 1
            current = characters[time % cycle]
    # 3. rstrip输出
    for i in range(size * 2):
        print(result[i].rstrip())
    
if __name__ == '__main__':
    import doctest
    doctest.testmod()