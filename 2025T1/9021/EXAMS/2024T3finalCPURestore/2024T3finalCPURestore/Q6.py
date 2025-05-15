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
from collections import defaultdict
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
    # 1. 读文件
    with open("dictionary.txt", 'r') as file:
        words_dic = [w.upper().strip() for w in file if w.strip()]
    dic = defaultdict(list)
    length = set()
    # 2. 逐位匹配
    for w in words_dic: # 对于每个字典里的词
        i, j = 0, 0
        while i < len(word):
            while j < len(w): # 两层while，对于每个位拿字典里的词匹配，看清是拿谁匹配谁
                if i < len(word) and j < len(w):
                    if w[j] == word[i]: # 如果匹配都往后挪一位，不匹配把词挪一位
                        i += 1
                        j += 1
                    else:
                        j += 1
                else: # 如果有一个词越界就break
                    break
            if j == len(w): # 如果被匹配的到了底
                break
        if i == len(word):
            length.add(len(w))
            dic[len(w)].append(w)
    if not dic: # 永远要注意空输入输出
        return []
    return sorted(dic[min(list(length))]) # 最小长度的字典值

if __name__ == '__main__':
    import doctest
    doctest.testmod()