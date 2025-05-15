# COMP9021 19T3 - Rachid Hamadi
# Sample Exam Question 8
from itertools import permutations

'''
Will be tested with letters a string of DISTINCT UPPERCASE letters only.
'''


def f(letters):
    '''
    >>> f('ABCDEFGH')
    There is no solution
    >>> f('GRIHWSNYP')
    The pairs of words using all (distinct) letters in "GRIHWSNYP" are:
    ('SPRING', 'WHY')
    >>> f('ONESIX')
    The pairs of words using all (distinct) letters in "ONESIX" are:
    ('ION', 'SEX')
    ('ONE', 'SIX')
    >>> f('UTAROFSMN')
    The pairs of words using all (distinct) letters in "UTAROFSMN" are:
    ('AFT', 'MOURNS')
    ('ANT', 'FORUMS')
    ('ANTS', 'FORUM')
    ('ARM', 'FOUNTS')
    ('ARMS', 'FOUNT')
    ('AUNT', 'FORMS')
    ('AUNTS', 'FORM')
    ('AUNTS', 'FROM')
    ('FAN', 'TUMORS')
    ('FANS', 'TUMOR')
    ('FAR', 'MOUNTS')
    ('FARM', 'SNOUT')
    ('FARMS', 'UNTO')
    ('FAST', 'MOURN')
    ('FAT', 'MOURNS')
    ('FATS', 'MOURN')
    ('FAUN', 'STORM')
    ('FAUN', 'STROM')
    ('FAUST', 'MORN')
    ('FAUST', 'NORM')
    ('FOAM', 'TURNS')
    ('FOAMS', 'RUNT')
    ('FOAMS', 'TURN')
    ('FORMAT', 'SUN')
    ('FORUM', 'STAN')
    ('FORUMS', 'NAT')
    ('FORUMS', 'TAN')
    ('FOUNT', 'MARS')
    ('FOUNT', 'RAMS')
    ('FOUNTS', 'RAM')
    ('FUR', 'MATSON')
    ('MASON', 'TURF')
    ('MOANS', 'TURF')
    '''
    dictionary = 'dictionary.txt'
    solutions = []
    # Insert your code here
    #先打开txt
    with open(dictionary) as file:
        
        dictionary = set([line.strip() for line in file
                          if len(line.strip()) == len(set(line.strip()))])


    #permutations 是输出letters里面的元素能够组合成的所有单词情况
    # i 是单词长度 例如i=2时 permutations(letters,2)就是用letters能组成的所有长度为2
    #的单词,用x在组成的单词中遍历
    #words的结果可能是多个
    words = sorted(
        ["".join(x) for i in range(2, len(letters))
         for x in permutations(letters, i)
         if "".join(x) in dictionary])
    # 看剩下的字母能不能组成单词
    #因为words结果是多个，所以需要用for循环
    for word in words:
        new_letters = set(letters) - set(word)
        new_words = sorted(["".join(x)
                            for x in permutations(new_letters, len(new_letters))
                            if "".join(x) in dictionary])
        for new_word in new_words:
            if (word, new_word) not in solutions \
                    and (new_word, word) not in solutions:
                solutions.append((word, new_word))

    if not solutions:
        print('There is no solution')
    else:
        print(f'The pairs of words using all (distinct) letters in "{letters}" are:')
        for solution in solutions:
            print(solution)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
