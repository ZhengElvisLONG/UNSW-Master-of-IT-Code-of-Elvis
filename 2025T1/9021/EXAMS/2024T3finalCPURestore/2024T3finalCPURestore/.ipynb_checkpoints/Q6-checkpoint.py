# Returns the list of all words in dictionary.txt, expected to be stored
# in the working directory, whose length is MINIMAL and that contain all 
# letters in "word", in the same order
# so if "word" is of from c1c2c3c4...cn, the solution is the list of 
# words of minimal length in dictionary.txt that are of the form *c1*c2*c3*c4*...*cn*
# where each occurecne of * denotes any (possible empty) sequence of letters.

# The words in the returned list appear in lexicographic order
# (in the order they occur in dictionaty.txt)

# You can assue that the argument to f() is a nonempty string of nothing
# but uppercase letters.

# Tip: find() method of str class is useful.

def f(word):
    '''
    >>> f('QWERTYUIOP')
    []
    >>> f('KIOSKS')
    []
    >>> f('INDUCTIVELY')
    ['INDUCTIVELY']
    >>> f('ITEGA')
    ['INTEGRAL']
    >>> f('ARON')
    ['AARON', 'AKRON', 'APRON', 'ARGON', 'ARSON', 'BARON']
    >>> f('EOR')
    ['EMORY', 'ERROR', 'TENOR']
    >>> f('AGAL')
    ['ABIGAIL', 'MAGICAL']
    '''
    return []
    # Replace the return statement above with your code.

if __name__ == '__main__':
    import doctest
    doctest.testmod()