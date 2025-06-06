# Written by *** for COMP9021
#
# Defines a function f() that takes a list as argument,
# that you can assume is a permutation of {0, ..., n}
# for some integer n >= 0.
# The function returns a list that is defined according
# to the example where the input list is
# [0, 2, 12, 3, 4, 6, 1, 9, 7, 10, 8, 11, 5].
# - Values smaller than indexes:
#   The index of 1 is 6, the index of 7 is 8,
#   the index of 8 is 10, and the index of 5 is 12.
# - Values equal to indexes: 0, 3, 4, 11.
# - Values larger than indexes:
#   The index of 2 is 1, the index of 12 is 2,
#   the index of 6 is 5, the index of 9 is 7
#   and the index of 10 is 9.
# [1, 7, 8, 5, 0, 3, 4, 11, 2, 12, 6, 9, 10] is returned.
#
# Defines a function g() that takes a list as argument,
# that you can assume is a permutation of {1, ..., n}
# for some integer n >= 1.
# The function returns a dictionary D, defined according
# to the example where the input list is
# [8, 9, 2, 6, 4, 5, 3, 1, 10, 7].
# - The first integer that comes after 8 in the list and that is
#   greater than 8 is 9, and the first integer that comes after 9
#   in the list and that is greater than 9 is 10.
#   D maps 1 to [0, 8, 9, 10].
# - What is left of the list is [2, 6, 4, 5, 3, 1, 7]
#   The first integer that comes after 2 in the list and that is
#   greater than 2 is 6, and the first integer that comes after 6
#   in the list and that is greater than 6 is 7.
#   D maps 2 to [0, 2, 6, 7].
# - What is left of the list is [4, 5, 3, 1]
#   The first integer that comes after 4 in the list and that is
#   greater than 4 is 5.
#   D maps 3 to [0, 4, 5].
# - What is left of the list is [3, 1]
#   No integer in the list after 3 is greater than 3.
#   D maps 4 to [0, 3].
# - What is left of the list is [1]
#   D maps 5 to [0, 1].


def f(L):
    result = []
    for i in range(len(L)):
        if L[i] < i:
            result.append(L[i])
    for i in range(len(L)):
        if L[i] == i:
            result.append(L[i])
    for i in range(len(L)):
        if L[i] > i:
            result.append(L[i])
    return result
# print(f([0, 2, 12, 3, 4, 6, 1, 9, 7, 10, 8, 11, 5]))

def g(L):
    D = {}
    time = 0
    while L:
        time += 1
        maximum = 0
        row = []
        initial = L[0]
        delist = []
        for i in range(len(L)):
            if L[i] > maximum:
                maximum = L[i]
                # L.pop(i)
                delist.append(i)
                row.append(L[i])
        row.reverse()
        row.append(0)
        row.reverse()
        D[time] = row
        for item in delist[::-1]:
            L.pop(item)
    return D
print(g([8, 9, 2, 6, 4, 5, 3, 1, 10, 7]))