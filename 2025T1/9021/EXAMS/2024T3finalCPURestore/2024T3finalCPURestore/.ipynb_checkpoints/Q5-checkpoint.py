from collections import defaultdict
def f(L):
    """
    >>> f([0, 0, 0])
    The members of L that are sums of two previous terms are: 
        0: 0 + 0
    >>> f([1, 1, 0])
    The members of L that are sums of two previous terms are: 
    >>> f([1, 1, 0, 1])
    The members of L that are sums of two previous terms are: 
        1: 1 + 0
    >>> f([1, 1, 0, 1, 2])
    The members of L that are sums of two previous terms are: 
        1: 1 + 0
        2: 1 + 1
    >>> f([1, 0, 2, 0, 3, 3, 3, 3, 1, 0, 3, 0, 3, 3, 0])
    The members of L that are sums of two previous terms are: 
        0: 0 + 0
        1: 1 + 0
        3: 1 + 2
    >>> f([3, 3, 0, 2, 4, 3, 3, 2])
    The members of L that are sums of two previous terms are: 
        2: 0 + 2
        3: 3 + 0
    >>> f([0, 1, 1, 5, 2, 4, 4, 3, 0, 2, 6, 6, 5, 7, 4])
    The members of L that are sums of two previous terms are: 
        1: 0 + 1
        2: 0 + 2
        3: 1 + 2
        4: 0 + 4
        5: 0 + 5
        6: 0 + 6
        7: 1 + 6
    """
    pass
    # REPLACE THE PASS STATEMENT ABOVE WITH YOUR CODE.
            
    
if __name__ == '__main__':
    import doctest
    doctest.testmod()