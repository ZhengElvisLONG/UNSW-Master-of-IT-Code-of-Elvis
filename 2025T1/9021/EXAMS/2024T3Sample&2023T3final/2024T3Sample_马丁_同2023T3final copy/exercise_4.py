# You can assume that the first two arguments to rectangle() are
# integers at least equal to 0, and that the third argument, if any,
# is a string consisting of an uppercase letter.
#
# The rectangle is read by going down the first column (if it exists),
# up the second column (if it exists), down the third column (if it exists),
# up the fourth column  (if it exists)...
#
# Hint: ord() and chr() are useful.

def next(letter):
    if letter == 'Z':
        return 'A'
    return chr(ord(letter) + 1)

def rectangle(width, height, starting_from='A'):
    '''
    >>> rectangle(0, 0)
    >>> rectangle(10, 1, 'V')
    VWXYZABCDE
    >>> rectangle(1, 5, 'X')
    X
    Y
    Z
    A
    B
    >>> rectangle(10, 7)
    ANOBCPQDER
    BMPADORCFQ
    CLQZENSBGP
    DKRYFMTAHO
    EJSXGLUZIN
    FITWHKVYJM
    GHUVIJWXKL
    >>> rectangle(12, 4, 'O')
    OVWDELMTUBCJ
    PUXCFKNSVADI
    QTYBGJORWZEH
    RSZAHIPQXYFG
    '''
    # 1. 建立需要转置的矩阵
    result = [["" for _ in range(height)] for _ in range(width)]
    # 2. 填充并赋予蛇形
    for i in range(width):
        for j in range(height):
            result[i][j] = starting_from
            starting_from = chr((ord(starting_from) + 1 - ord('A')) % 26 + ord('A')) # 记住常用
        if i % 2: # 如果是奇数行，倒置，就是蛇形
            result[i].reverse()
    # 3. 转置并输出
    result = list(map(list, zip(*result)))
    for i in range(height):
        print("".join(result[i])) # 如果是字符列表可以这么操作，如果是数字就要做格式调整

if __name__ == '__main__':
    import doctest
    doctest.testmod()
