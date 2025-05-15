# You can assume that word_pairs() is called with a string of
# uppercase letters as agument.
#
# dictionary.txt is stored in the working directory.
#
# Outputs all pairs of distinct words in the dictionary file, if any,
# that are made up of all letters in available_letters
# (if a letter in available_letters has n occurrences,
# then there are n occurrences of that letter in the combination
# of both words that make up an output pair).
#
# The second word in a pair comes lexicographically after the first word.
# The first words in the pairs are output in lexicographic order
# and for a given first word, the second words are output in
# lexicographic order.
#
# Hint: If you do not know the imported Counter class,
#       experiment with it, passing a string as argument, and try
#       arithmetic and comparison operators on Counter objects.


from collections import Counter
dictionary_file = 'dictionary.txt'


def word_pairs(available_letters):
    '''
    >>> word_pairs('ABCDEFGHIJK')
    >>> word_pairs('ABCDEF')
    CAB FED
    >>> word_pairs('ABCABC')
    >>> word_pairs('EOZNZOE')
    OOZE ZEN
    ZOE ZONE
    >>> word_pairs('AIRANPDLER')
    ADRENAL RIP
    ANDRE APRIL
    APRIL ARDEN
    ARID PLANER
    ARLEN RAPID
    DANIEL PARR
    DAR PLAINER
    DARER PLAIN
    DARNER PAIL
    DARPA LINER
    DENIAL PARR
    DIRE PLANAR
    DRAIN PALER
    DRAIN PEARL
    DRAINER LAP
    DRAINER PAL
    DRAPER LAIN
    DRAPER NAIL
    ERRAND PAIL
    IRELAND PAR
    IRELAND RAP
    LAIR PANDER
    LAND RAPIER
    LAND REPAIR
    LANDER PAIR
    LARDER PAIN
    LEARN RAPID
    LIAR PANDER
    LINDA RAPER
    NADIR PALER
    NADIR PEARL
    NAILED PARR
    PANDER RAIL
    PLAN RAIDER
    PLANAR REID
    PLANAR RIDE
    PLANER RAID
    RAPID RENAL
    '''
    pass
    # REPLACE PASS ABOVE WITH YOUR CODE
                

if __name__ == '__main__':
    import doctest
    doctest.testmod()
