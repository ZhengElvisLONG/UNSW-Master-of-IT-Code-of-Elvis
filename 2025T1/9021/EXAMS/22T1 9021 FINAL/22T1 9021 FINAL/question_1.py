# Will be tested only with number an integer.
#
# If number is positive, returns a positive integer.
# If number is negative, returns a negative integer.
#
# The digits of the returned integer are the digits of number
# ordered from largest to smallest.

def reorder(number):
    '''
    >>> reorder(0)
    0
    >>> reorder(2)
    2
    >>> reorder(-33)
    -33
    >>> reorder(202)
    220
    >>> reorder(242242)
    442222
    >>> reorder(-3210123)
    -3322110
    >>> reorder(22659717106393887106)
    99887776665332211100
    '''
    # 1. 对于把数字变成字符串处理的问题，首先处理正负
    result = ""
    # 2. 用字典对每一位做储存
    dic = {}
    for i in range(10):
        dic[i] = 0
    positive = 1
    tostr = str(abs(number))
    if number < 0:
        positive = -1
    # 3. 处理好“空输入输出”
    elif number == 0:
        print(0)
        return
    # 4. 处理字典储存
    for digit in tostr:
        dic[int(digit)] += 1
    for i in range(10):
        while dic[i] != 0:
            result += str(i)
            dic[i] -= 1
    print(f"{int(result[::-1]) * positive}")

if __name__ == '__main__':
    import doctest
    doctest.testmod()
