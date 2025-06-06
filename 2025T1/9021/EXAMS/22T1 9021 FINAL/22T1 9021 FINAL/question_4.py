from itertools import zip_longest


# The carry over of the sum of all units is discarded.
# The carry over of the sum of all multiples of 10 is discarded.
# The carry over of the sum of all multiples of 100 is discarded.
# ...
# Will be tested with at least one argument,
# all arguments being positive integers (possibly equal to 0).

def sum_discarding_carry_overs(*numbers):
    '''
    >>> sum_discarding_carry_overs(0)
    0
    >>> sum_discarding_carry_overs(3, 4)
    7
    >>> sum_discarding_carry_overs(4, 6)
    0
    >>> sum_discarding_carry_overs(7, 5)
    2
    >>> sum_discarding_carry_overs(0, 1, 2, 3)
    6
    >>> sum_discarding_carry_overs(0, 1, 2, 3, 4)
    0
    >>> sum_discarding_carry_overs(0, 1, 2, 3, 4, 5)
    5
    >>> sum_discarding_carry_overs(91, 19)
    0
    >>> sum_discarding_carry_overs(38, 49)
    77
    >>> sum_discarding_carry_overs(58, 59)
    7
    >>> sum_discarding_carry_overs(2314, 5968)
    7272
    >>> sum_discarding_carry_overs(3452, 2324, 36372, 75401)
    6449
    >>> sum_discarding_carry_overs(9054, 3, 3577, 78, 452563)
    454055
    '''
    # REPLACE THE RETURN STATEMENT ABOVE WITH YOUR CODE
    lst = list(numbers)
    max_len = 0
    prt = 0
    for i in range(len(lst)):
        lst[i] = str(lst[i])
        if max_len < len(lst[i]):
            max_len = len(lst[i])
    result = [0 for _ in range(max_len)]
    for i in range(len(lst)):
        lst[i] = '0' * (max_len - len(lst[i])) + lst[i]
    for i in range(len(lst)):
        for j in range(max_len):
            result[j] = (result[j] + int(lst[i][j])) % 10
    for j in range(max_len):
        prt = 10 * prt + result[j]
    print(prt)



if __name__ == '__main__':
    import doctest
    doctest.testmod()
