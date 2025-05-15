# Exercise 6: Longest Word from Available Letters
# You can assume that longest_word_from_letters() is called with a string of
# uppercase letters as argument.
#
# dictionary.txt is stored in the working directory.
#
# Finds the longest word(s) in the dictionary file that can be formed
# using only the letters available in available_letters (respecting counts).
# If multiple words share the same maximum length, output all of them in
# lexicographical order, each on a new line.
# If no word can be formed, output nothing.
#
# Hint: Use collections.Counter.

from collections import Counter

dictionary_file = 'dictionary.txt'

def longest_word_from_letters(available_letters):
    """
    Finds the longest word(s) formable from available_letters.
    
    >>> longest_word_from_letters('ABC') # A, AB, BA, BC, CA, CB, ABC...
    A
    B
    C
    # Assuming dictionary contains A, B, C, AB, BA, CAB etc.
    # Let's refine doctest based on a realistic dictionary.txt
    # Assuming dictionary.txt has standard English words.
    >>> longest_word_from_letters('TREASURE') # RARE, RATE, SEAT, SURE, TEAR, TRUE, TREAT, ...
    ERRATA
    REARER
    RESEAT
    RESTER
    RETEAR
    SATURN
    SERR ATE
    TEASER
    TERRAS
    TREASURE
    >>> longest_word_from_letters('PYTHON') # ON, NO, HOP, HOT, NTH, PHY, POT, ...
    PYTHON
    TYPHON
    >>> longest_word_from_letters('PROGRAMMING') # PROGRAM, PROM, RAM, ...
    PROGRAMING
    PROGRAMMING
    >>> longest_word_from_letters('XYZ') # Assuming no words with X, Y, Z
    >>> longest_word_from_letters('AEIOU') # Assuming dictionary has vowels
    AEIOU
    """
    target_count = Counter(available_letters)
    longest_len = 0
    longest_words = []
    
    try:
        with open(dictionary_file) as f:
            words = [word.strip().upper() for word in f if word.strip()]
    except FileNotFoundError:
        print(f"Error: {dictionary_file} not found.")
        return

    for word in words:
        word_count = Counter(word)
        # Check if word can be formed from available letters
        can_form = True
        for char, count in word_count.items():
            if target_count[char] < count:
                can_form = False
                break
        
        if can_form:
            current_len = len(word)
            if current_len > longest_len:
                longest_len = current_len
                longest_words = [word]
            elif current_len == longest_len:
                longest_words.append(word)
                
    # Sort and print the longest words found
    longest_words.sort()
    for word in longest_words:
        print(word)

if __name__ == '__main__':
    import doctest
    # Note: Doctests depend heavily on the content of dictionary.txt
    # The provided doctests are illustrative and might need adjustment
    # based on the actual dictionary file used during testing.
    doctest.testmod()

