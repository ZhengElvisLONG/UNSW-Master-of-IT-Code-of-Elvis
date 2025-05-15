# You can assume that the first two arguments to rectangle() are
# integers at least equal to 0, and that the third argument, if any,
# is a string consisting of an uppercase letter.
#
# The rectangle is read by going down the first column (if it exists),
# up the second column (if it exists), down the third column (if it exists),
# up the fourth column  (if it exists)...
#
# Hint: ord() and chr() are useful.


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
    pass
    # REPLACE PASS ABOVE WITH YOUR CODE
        

if __name__ == '__main__':
    import doctest
    doctest.testmod()
