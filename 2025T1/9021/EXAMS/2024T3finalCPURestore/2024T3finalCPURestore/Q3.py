# Return an integer that is the integer passed as argument
# with all even digits including 0 'removed'
# In particular, if all digit are even, then 0 is returned

# You can assue that the argument to f() is an integer.

def f(n):
    '''
    >>> f(-12345667)
    -1357
    >>> f(0)
    0
    >>> f(1)
    1
    >>> f(-2)
    0
    >>> f(12334563)
    13353
    >>> f(-987654321098765)
    -97531975
    '''
    # 因为需要变成字符串处理，所以要提前把可能的负号提出来，设成+-1比bool合适
    isPositive = 1
    if n < 0:
        isPositive = -1
        n = -n
    result = ""
    # 从高到低提取每一位并判断能不能加进result
    while n:
        if n % 10 % 2 != 0:
            result = str(n % 10) + result # 注意加的顺序，不然会倒置
        n //= 10
    if not len(result):
        result = "0"
    return isPositive * int(result)

if __name__ == '__main__':
    import doctest
    doctest.testmod()