# Will be tested with letters a string of DISTINCT UPPERCASE letters only.

from collections import defaultdict
def f(letters):
    '''
    >>> f('ABCDEFGH')
    There is no solution.
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
    # INSERT YOUR CODE HERE
    with open(dictionary) as f:
        words = [word.strip().upper() for word in f]

    letters_set = set(letters)
    valid_words = [word for word in words if set(word).issubset(letters_set)]

    len_to_words = defaultdict(list)
    for word in valid_words:
        len_to_words[len(word)].append(word)

    total_len = len(letters)
    for len1 in range(1, total_len):
        len2 = total_len - len1
        if len2 < 1:
            continue
        words_len1 = len_to_words.get(len1, [])
        words_len2 = len_to_words.get(len2, [])
        for word1 in words_len1:
            remaining_letters = letters_set - set(word1)
            for word2 in words_len2:
                if set(word2) == remaining_letters:
                    pair = tuple(sorted((word1, word2)))
                    if pair not in solutions:
                        solutions.append(pair)
        solutions.sort()



    if not solutions:
        print('There is no solution.')
    else:
        print(f'The pairs of words using all (distinct) letters '
              f'in "{letters}" are:'
             )
        for solution in solutions:
            print(solution)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
