def f(grid):
    '''
    >>> f([["◾️", "◾️"],\
           ["◾️", "◾️"]])
      The horizontal words are:
    <BLANKLINE>
    <BLANKLINE>
      The vertical words are:
    <BLANKLINE>
    <BLANKLINE>
    >>> f([["O", "H"],\
           ["◾️", "◾️"]])
      The horizontal words are:
    OH
    <BLANKLINE>
      The vertical words are:
    <BLANKLINE>
    <BLANKLINE>
    >>> f([["◾️", "O"],\
           ["◾️", "H"]])
      The horizontal words are:
    <BLANKLINE>
    <BLANKLINE>
      The vertical words are:
    <BLANKLINE>
    OH
    >>> f([["◾️", "O"],\
           ["A", "H"]])
      The horizontal words are:
    <BLANKLINE>
    AH
      The vertical words are:
    <BLANKLINE>
    OH
    >>> f([["A", "R", "F", "◾️", "P", "B", "S", "◾️", "◾️"],\
           ["B", "A", "◾️", "◾️", "I", "C", "E", "D", "◾️"],\
           ["O", "H", "I", "S", "E", "E", "N", "O", "W"],\
           ["L", "A", "R", "K", "S", "◾️", "T", "W", "A"],\
           ["I", "S", "S", "A", "◾️", "O", "I", "N", "K"],\
           ["S", "H", "N", "◾️", "A", "R", "E", "P", "A"],\
           ["H", "E", "A", "D", "C", "A", "N", "O", "N"],\
           ["◾️", "S", "K", "E", "E", "◾️", "C", "U", "D"],\
           ["◾️", "◾️", "E", "N", "D", "◾️", "E", "R", "A"]])
      The horizontal words are:
    ARF
    PBS
    BA
    ICED
    OHISEENOW
    LARKS
    TWA
    ISSA
    OINK
    SHN
    AREPA
    HEADCANON
    SKEE
    CUD
    END
    ERA
      The vertical words are:
    ABOLISH
    RAHASHES
    IRSNAKE
    SKA
    DEN
    PIES
    ACED
    BCE
    ORA
    SENTIENCE
    DOWNPOUR
    WAKANDA
    '''
    pass
    # REPLACE THE PASS STATEMENT ABOVE WITH YOUR CODE.

if __name__ == '__main__':
    import doctest
    doctest.testmod()