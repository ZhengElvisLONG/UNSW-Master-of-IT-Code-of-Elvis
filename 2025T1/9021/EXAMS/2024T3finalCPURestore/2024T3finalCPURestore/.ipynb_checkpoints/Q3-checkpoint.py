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
    return 0
    # Replace the return statement above with your code.

if __name__ == '__main__':
    import doctest
    doctest.testmod()