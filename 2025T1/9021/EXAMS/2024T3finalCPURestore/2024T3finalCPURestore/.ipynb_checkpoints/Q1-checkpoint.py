# The second sequence is the first sequence in reverse order.

# In the first sequence, the gap between first and second terms.
# if any, is 1, and it keeps increasing 1 for the pairs 
# of successive terms that follow, if any.

# You can assue that the first argument to f() is an interger
# and the second argument to f() is an integer at least equal to 1.

def f(start=1, nb_of_terms=1):
    '''
    >>> f()
    ((1,), (1,))
    >>> f(1, 2)
    ((1, 2), (2, 1))
    >>> f(1, 3)
    ((1, 2, 4), (4, 2, 1))
    >>> f(1, 4)
    ((1, 2, 4, 7), (7, 4, 2, 1))
    >>> f(-10)
    ((-10,), (-10,))
    >>> f(-10, 2)
    ((-10, -9), (-9, -10))
    '''
    return (), ()
    # Replace the return statement above with your code.

if __name__ == '__main__':
    import doctest
    doctest.testmod()