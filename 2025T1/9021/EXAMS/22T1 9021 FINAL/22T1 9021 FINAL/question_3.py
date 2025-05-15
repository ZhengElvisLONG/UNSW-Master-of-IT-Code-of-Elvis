# Will be tested only with strictly positive integers for
# total_nb_of_letters and height.
#
# <BLANKLINE> is not output by the program, but
# doctest's way to refer to an empty line.
# For instance,
#    A
#    B
#    C
#    <BLANKLINE>
#    <BLANKLINE>
# means that 5 lines are output: first a line with A,
# then a line with B, then a line with C,
# and then 2 empty lines.
#
# Note that no line has any trailing space.

def f(total_nb_of_letters, height):
    '''
    >>> f(4, 1)
    ABCD
    >>> f(3, 5)
    A
    B
    C
    <BLANKLINE>
    <BLANKLINE>
    >>> f(4, 2)
    AD
    BC
    >>> f(5, 2)
    ADE
    BC
    >>> f(6, 2)
    ADE
    BCF
    >>> f(7, 2)
    ADE
    BCFG
    >>> f(8, 2)
    ADEH
    BCFG
    >>> f(9, 2)
    ADEHI
    BCFG
    >>> f(17,5)
    AJK
    BIL
    CHM
    DGNQ
    EFOP
    >>> f(100, 6)
    ALMXYJKVWHITUFGRS
    BKNWZILUXGJSVEHQT
    CJOVAHMTYFKRWDIPU
    DIPUBGNSZELQXCJOV
    EHQTCFORADMPYBKN
    FGRSDEPQBCNOZALM
    '''
    # INSERT YOUR CODE HERE
    # current = 'A'
    # result = ["" for _ in range((total_nb_of_letters + height - 1) // height)]
    # prt = ["" for _ in range((total_nb_of_letters + height - 1) // height)]
    # for idx in range((total_nb_of_letters + height - 1) // height):
    #     for _ in range(height):
    #         result[idx] += current
    #         current = 'A' if current == 'Z' else chr(ord(current) + 1)
    # for idx in range((total_nb_of_letters + height - 1) // height):
    #     if idx % 2:
    #         result[idx] = result[idx][::-1]
    # transposed = list(map(list, zip(*result)))
    # cols = (total_nb_of_letters + height - 1) // height
    
    # if total_nb_of_letters < cols * height:
    #     cnt = cols * height - total_nb_of_letters
    #     if cols % 2:
    #         for i in range(height - 1, height - 1 - cnt, -1):
    #             if i >= 0 and transposed[i]:
    #                 transposed[i].pop()
    #     else:
    #         for i in range(cnt):
    #             if i >= 0 and transposed[i]:
    #                 transposed[i].pop()
    # output = "\n".join(["".join(row) for row in transposed])
    # print(output)
    current = 'A'
    width = (total_nb_of_letters + height - 1) // height
    matrix = [[" " for _ in range(height)] for _ in range(width)]
    idx = 0
    for i in range(width):
        for j in range(height):
            if idx >= total_nb_of_letters:
                break
            matrix[i][j] = current
            current = chr((ord(current) + 1 - ord('A')) % 26 + ord('A'))
            idx += 1
        if i % 2:
            matrix[i].reverse()
    matrix = list(zip(*matrix))
    # for i in range(height):
    #     for j in range(width):
    #         if matrix[i][j] != " "
    #             print(matrix[i][j], end = "")
    #     print("")
    result = ["" for _ in range(height)]
    for i in range(height):
        result[i] = "".join(matrix[i]).rstrip()
        print(result[i])



if __name__ == '__main__':
    import doctest

    doctest.testmod()
