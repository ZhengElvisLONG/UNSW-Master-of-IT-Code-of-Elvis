# Return the list of Strictly INCREASING sub lists of the list L
# passed as argument. each of which is NOT a strict sublist of a 
# strictly increasing sublist of L

# Mapping a sublist ot the set of indexes in L of its elements.
# making those indexes minimal, the sublists are ordered in
# lexicographic order that mapping.

# You can assume that the argument to f() is a list of integers.

def f(L):
    '''
    >>> f([])
    []
    >>> f([1])
    [[1]]
    >>> f([1, 2])
    [[1, 2]]
    >>> f([2, 1])
    [[2], [1]]
    >>> f([1, 2, 3])
    [[1, 2, 3]]
    >>> f([1, 3, 2])
    [[1, 3], [1, 2]]
    >>> f([2, 1, 3])
    [[2, 3], [1, 3]]
    >>> f([2, 3, 1])
    [[2, 3], [1]]
    >>> f([3, 1, 2])
    [[3], [1, 2]]
    >>> f([3, 2, 1])
    [[3], [2], [1]]
    >>> f([9, 3, 1, 2, 9, 7])
    [[9], [3, 9], [3, 7], [1, 2, 9], [1, 2, 7]]
    >>> f([2, 8, 3, 8, 0, 9, 3, 7])
    [[2, 8, 9], [2, 3, 8, 9], [2, 3, 7], [0, 9], [0, 3, 7]]
    >>> f([17, 0, 14, 15, 19, 6, 16, 4, 5, 1])
    [[17, 19], [0, 14, 15, 19], [0, 14, 15, 16], [0, 6, 16], [0, 4, 5], [0, 1]]
    '''
    return []
    # Replace the return statement above with your code.

if __name__ == '__main__':
    import doctest
    doctest.testmod()