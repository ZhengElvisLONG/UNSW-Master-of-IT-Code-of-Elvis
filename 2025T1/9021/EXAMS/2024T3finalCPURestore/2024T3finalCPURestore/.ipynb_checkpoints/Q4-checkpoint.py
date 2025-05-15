# Return a dict whose keys are all members of the agrument 
# L to f(), whth as associated value for a member n of L 
# the sorted list, WHITHOUT REPETITIONS, of all members of 
# L that occur RIGHT AFTER some occurrence of n in L.

# We consider that the first member of L occurs right after
# the last member of L ( as if L was ring); in case L has 
# only one term, then that term is both the first and the last of L.

# You can assue that the argument to f() is a nonempty list of integers.

from collections import defaultdict
def f(L):
    '''
    >>> D = f([1])
    >>> {e: D[e] for e in sorted(D)}
    {1: [1]}
    >>> D = f([1, 1, 1])
    >>> {e: D[e] for e in sorted(D)}
    {1: [1]}
    >>> D = f([1, 2, 1, 2])
    >>> {e: D[e] for e in sorted(D)}
    {1: [2], 2: [1]}
    >>> D = f([1, 2, 1, 2, 1])
    >>> {e: D[e] for e in sorted(D)}
    {1: [1, 2], 2: [1]}
    >>> D = f([-5, 5, 5, -4, -2, 4, 1, 3, -2, 5])
    >>> {e: D[e] for e in sorted(D)}
    {-5: [5], -4: [-2], -2: [4, 5], 1: [3], 3: [-2], 4: [1], 5: [-5, -4, 5]}
    '''
    return {}
    # Replace the return statement above with your code.
    

if __name__ == '__main__':
    import doctest
    doctest.testmod()