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
    idx = set()
    dic = {}
    for i in range(len(L)): # 硬要用傻方法，不然输出不对
        for j in range(len(L)):
            for k in range(len(L)):
                if L[i] + L[j] == L[k] and i < j < k and L[k] not in dic:
                    dic[L[k]] = (L[i], L[j]) # 只取第一个
                    idx.add(L[k])
    print("The members of L that are sums of two previous terms are: ")
    for i in sorted(dic):
        print(f"    {i}: {dic[i][0]} + {dic[i][1]}")

if __name__ == '__main__':
    import doctest
    doctest.testmod()