# You can assume that the argument to solve() is of the form
# x+y=z where:
# - x, y and z are NONEMPTY sequences of UNDERSCORES and DIGITS;
# - there can be any number of spaces (possibly none) before x,
#   between x and +, between + and y, between y and =, between = and z,
#   and after z.
#
# ALL OCCURRENCES OF _ ARE MEANT TO BE REPLACED BY THE SAME DIGIT.
#
# Note that sequences of digits such as 000 and 00037 represent
# 0 and 37, consistently with what int('000') and int('00037') return,
# respectively.
#
# When there is more than one solution, solutions are output from
# smallest to largest values of _.
#
# Note that an equation is always output with a single space before and after
# + and =, with no leading nor trailing spaces, and without extra leading 0s
# in front of an integer.
#
# Hint: The earlier you process underscores, the easier,
#       and recall what dir(str) can do for you.


def solve(equation):
    '''
    >>> solve('1 + 2 = 4')
    No solution!
    >>> solve('123 + 2_4 = 388')
    No solution!
    >>> solve('1+2   =   3')
    1 + 2 = 3
    >>> solve('123 + 2_4 = 387')
    123 + 264 = 387
    >>> solve('_23+234=__257')
    23 + 234 = 257
    >>> solve('   __   +  _____   =     ___    ')
    0 + 0 = 0
    >>> solve('__ + __  = 22')
    11 + 11 = 22
    >>> solve('   012+021   =   00__   ')
    12 + 21 = 33
    >>> solve('_1   +    2   =    __')
    31 + 2 = 33
    >>> solve('0 + _ = _')
    0 + 0 = 0
    0 + 1 = 1
    0 + 2 = 2
    0 + 3 = 3
    0 + 4 = 4
    0 + 5 = 5
    0 + 6 = 6
    0 + 7 = 7
    0 + 8 = 8
    0 + 9 = 9
    '''
    # 1. 字符串处理，提取abc三个元素
    equation = equation.replace(" ", "") # 先把空格处理掉
    lst = equation.split("+") # split拆分成不同模块
    a = lst[0]
    lst = lst[1].split("=")
    b, c = lst[0], lst[1]
    # 2. 查看是否需要替换
    need_replace = False
    if "_" in a + b + c:
        need_replace = True
    # 3. 如果不需要替换，直接验证
    if not need_replace:
        a, b, c = int(a), int(b), int(c) # 注意要int化
        if a + b == c:
            print(f"{a} + {b} = {c}")
        else:
            print("No solution!")
        return # 输出以后直接返回，防止被下面代码干扰
    # 4. 需要替换，统一替换验证
    has_solution = False
    for i in range(10):
        i = str(i)
        na, nb, nc = a, b, c # 注意用新变量存，不然会影响后面循环
        na, nb, nc = int(na.replace("_", i)), int(nb.replace("_", i)), int(nc.replace("_", i))
        if na + nb == nc:
            has_solution = True
            print(f"{na} + {nb} = {nc}") # 不用排序，因为已经按序替换
    if not has_solution:
        print("No solution!")

if __name__ == '__main__':
    import doctest
    doctest.testmod()