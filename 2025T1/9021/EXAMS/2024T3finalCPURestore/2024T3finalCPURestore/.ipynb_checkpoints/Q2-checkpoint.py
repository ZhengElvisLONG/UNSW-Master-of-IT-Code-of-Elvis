# NO line has any trailing space.

# You can assue that the first argument to f() is an intetger at least
# equal to 2 and the second argument to f() is a nonempty string.

# The output is printes out, not retuened.

from itertools import cycle

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
    pass
    # REPLACE THE PASS STATEMENT ABOVE WITH YOUR CODE.
    
if __name__ == '__main__':
    import doctest
    doctest.testmod()