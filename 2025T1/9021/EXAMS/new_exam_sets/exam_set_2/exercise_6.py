# Exercise 6: Disjoint Word Pairs
# You can assume that disjoint_word_pairs() is called with a string of
# uppercase letters as argument.
#
# dictionary.txt is stored in the working directory.
#
# Outputs all pairs of distinct words in the dictionary file, if any,
# that together are made up of all letters in available_letters
# (if a letter in available_letters has n occurrences,
# then there are n occurrences of that letter in the combination
# of both words that make up an output pair).
# Additionally, the two words in a pair must share NO common letters.
#
# The second word in a pair comes lexicographically after the first word.
# The first words in the pairs are output in lexicographic order
# and for a given first word, the second words are output in
# lexicographic order.
#
# Hint: Use collections.Counter and set operations.

from collections import Counter

dictionary_file = 'dictionary.txt'

def disjoint_word_pairs(available_letters):
    """
    Finds pairs of distinct words with no common letters, using all available letters.
    
    >>> disjoint_word_pairs('ABCDEFGHIJK') # Likely no solution
    >>> disjoint_word_pairs('ABCDEF') # CAB and FED share E, F, D, C, A, B - not disjoint
    >>> disjoint_word_pairs('TOPCAR') # POT CAR (disjoint), TOP ARC (disjoint)
    ARC TOP
    CAR POT
    >>> disjoint_word_pairs('GOSTOP') # STOP GO (disjoint)
    GO STOP
    >>> disjoint_word_pairs('LASERBEAM') # BEAM LASER (disjoint)
    BEAM LASER
    >>> disjoint_word_pairs('PYTHONCODE') # No disjoint pairs using all letters?
    >>> disjoint_word_pairs('TESTSAMPLE') # SAMPLE TEST (share S, T, E)
    """
    # target_count = Counter(available_letters)
    # solutions = []
    
    # try:
    #     with open(dictionary_file) as f:
    #         words = [word.strip().upper() for word in f if word.strip()]
    # except FileNotFoundError:
    #     print(f"Error: {dictionary_file} not found.")
    #     return

    # # Pre-filter words based on letter availability
    # valid_words = []
    # for word in words:
    #     word_count = Counter(word)
    #     if len(word) > 0 and len(word) < len(available_letters) and \
    #        all(word_count[char] <= target_count[char] for char in word_count):
    #         valid_words.append((word, word_count))
            
    # # Find all valid pairs
    # for i, (word1, count1) in enumerate(valid_words):
    #     remaining_count = target_count - count1
    #     # Check if remaining count is valid (all counts >= 0)
    #     if all(c >= 0 for c in remaining_count.values()):
    #         # Find potential second words
    #         for j, (word2, count2) in enumerate(valid_words[i+1:], i+1):
    #             if count2 == remaining_count:
    #                 # Check for disjoint letter sets
    #                 if not (set(word1) & set(word2)):
    #                     # Ensure lexicographical order within the pair for output
    #                     pair = tuple(sorted((word1, word2)))
    #                     solutions.append(pair)
                        
    # # Remove duplicates (if any, though logic should prevent them) and sort
    # unique_solutions = sorted(list(set(solutions)))
    
    # # Print solutions
    # for pair in unique_solutions:
    #     print(f"{pair[0]} {pair[1]}")

if __name__ == '__main__':
    import doctest
    doctest.testmod()

