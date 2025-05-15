# Exercise 6: Word Triplets
# You can assume that word_triplets() is called with a string of
# uppercase letters as argument.
#
# dictionary.txt is stored in the working directory.
#
# Outputs all triplets of distinct words in the dictionary file, if any,
# that are made up of all letters in available_letters
# (if a letter in available_letters has n occurrences,
# then there are n occurrences of that letter in the combination
# of the three words that make up an output triplet).
#
# The words in a triplet are output in lexicographic order.
# The triplets are output in lexicographic order based on the first word,
# then the second word, then the third word.
#
# Hint: Consider using collections.Counter for efficient letter counting.

from collections import Counter
from itertools import combinations

dictionary_file = 'dictionary.txt'

def word_triplets(available_letters):
    """
    Finds triplets of distinct words using all available letters.
    
    >>> word_triplets('ABCDEFGHI') # Likely no solution for short strings
    >>> word_triplets('PROGRA') # Too short
    >>> word_triplets('TEACHING') # Example with a possible solution
    ACE GHI NT
    >>> word_triplets('PYTHONCODE') # Example with potential solutions
    CENT HOOP DY
    CODE HOP TYNE
    CODE HOT PENY
    COPE HOD TYNE
    COPE HOT DENY
    COPEN HOT DYE
    HOPE COD TYNE
    HOPE COT DENY
    OPEN CHOD TYE
    PHONE COD TEY
    PHONE COT DYE
    PONY CHODE T
    PONY CODE HT
    PONY HOC TED
    PONY HOT CDE
    TYPE CHON ODE
    TYPE CODE HON
    TYPE HOE COND
    TYPE HON CODE
    >>> word_triplets('ALGORITHMS') # Longer example
    AH GIRL MOST
    AH GIST MORL
    AH GRIM SLOT
    AH GRIT SLOM
    AH LIST MOGR
    AH LOGS TRIM
    AH LOST GRIM
    AIL GHOST MR
    AIR GHOST LM
    AIR LOGS MHT
    AIR MOST HLG
    AIR SLOT HMG
    AL GHOST RIM
    AL GRIM HOST
    AL GRIT SHOM
    AL SHIRT MOG
    AL SORT GHIM
    ALSO GRIM HT
    ALSO GRIT HM
    ALSO MIGHT R
    ALSO RIGHT M
    GASH LOR MIT
    GASH LOT RIM
    GASH ROT LIM
    GHOST RAIL M
    GHOST RIAL M
    GIRL HOST AM
    GIRL MATH OS
    GIRL MOST AH
    GIRL SHAM OT
    GIRL SHOT AM
    GIRT SHAM LO
    GIRT SHMO AL
    GIST LOAM HR
    GIST MORAL H
    GIST MORL AH
    GIST ROAM HL
    GOAL SHIRT M
    GOAL TRIM HS
    GOAT SHIRL M
    GOAT SHRIL M
    GOSH RAIL MT
    GOSH RIAL MT
    GOSH TRAIL M
    GOSH TRIAL M
    GOT SHIRL AM
    GOT SHRIL AM
    GRIM HOST AL
    GRIM LOTS AH
    GRIM SLOT AH
    GRIT SHAM LO
    GRIT SHMO AL
    GRIT SLOM AH
    HAIL GORM ST
    HAIL GROT MS
    HAIL MORT GS
    HAIL MOST RG
    HAIL STORM G
    HALO GRIM ST
    HALO Grist M
    HALO MIST RG
    HALO RIMS GT
    HALO SMIT RG
    HALO TRIMS G
    HARM GIST LO
    HARM GITS LO
    HARM LOGS IT
    HARM LOTS GI
    HARM SLIT GO
    HARM SLOT GI
    HART Gismo L
    HART GIST LM
    HART LOGS IM
    HART SLIM GO
    HART SLOG IM
    HOGS RAIL MT
    HOGS RIAL MT
    HOGS TRAIL M
    HOGS TRIAL M
    HOLM Grist A
    HOLM RAGS IT
    HOLM RATS GI
    HOLM STAR GI
    HOLM STRIA G
    HOLM TARS GI
    HOLM TSAR GI
    HOST GIRL AM
    HOST GRIM AL
    HOST MAIL RG
    HOST RAIL MG
    HOST RIAL MG
    HOST SLIM ARG
    HOST TRIM LAG
    HOST TRIM GAL
    HOT GIRL MAS
    HOT GRAMS LI
    HOT LAGS RIM
    HOT LARGE ISM
    HOT MARLS GI
    HOT RAGS LIM
    HOT SLAG RIM
    Iota Harl Ms
    Iota Rash Lm
    LAIR GHOST M
    LAIR GOT SHM
    LAM GHOST IR
    LAM GRIST HO
    LAM SHIRT GO
    LAM THRO GIS
    LASH GORM IT
    LASH GROT IM
    LASH MORT GI
    LASH TROG IM
    LAST GRIM HO
    LAST MOG HIR
    LAST MORG HI
    LAST OHM RIG
    LOAM Grist H
    LOAM Grist H
    LOAM RAGS HIT
    LOAM RASH GIT
    LOAM RATH GIS
    LOAM SHIRT G
    LOAM STAR HIG
    LOAM TRAGS HI
    LOGS MATH IR
    LOGS RATH IM
    LOGS TRIM AH
    LOST GRIM AH
    LOST HARM GI
    LOST MAR H GI
    LOST MATH RIG
    LOST RAG HIM
    LOST TAG RHIM
    LOT GIRL MASH
    LOT GRIM ASH
    LOT HAGS RIM
    LOT HARM GIS
    LOT RAGS HIM
    LOT SHAG RIM
    MAIL GHOST R
    MAIL GOT SHR
    MARL GHOST I
    MARL GIST HO
    MARL GOT HIS
    MARL HOGS IT
    MARL HOST GI
    MARL SHOT GI
    MARL SITH GO
    MARL THIS GO
    MARSH GILT O
    MARSH GOT LI
    MART GHOST LI
    MART GIST HOL
    MART HOGS IL
    MART SHOG LI
    MART SLOG HI
    MATH GIRL OS
    MATH LOGS IR
    MATH RIGS LO
    MATH SLOG IR
    MIST GIRL HOA
    MIST Harl Go
    MIST Hoar Gl
    MIST Hora Gl
    MIST RAG HOL
    MIST TAG HORL
    MOG SHIRT AL
    MORG SHALT I
    MORG SHIRT LA
    MORL GIST AH
    MORL TAGS HI
    MORT GASH LI
    MORT HAGS IL
    MORT SHAG LI
    MOST GIRL AH
    MOST Harl Gi
    MOST Hoar Gl
    MOST Hora Gl
    MOST RAG HIL
    MOST TAG HIRL
    OATH GIRL MS
    OATH GRIM LS
    OATH GRISL M
    OATH SLIM RG
    OATH SMIRL G
    OH GIRL MAST
    OH GIRL MATS
    OH GIRL STAM
    OH GRIM LAST
    OH GRIM SALT
    OH GRIM SLAT
    OH GRIST LAM
    OH RAGS MILT
    OH RAGS SLIM T
    OH RIMS GALT
    OH SLIM GRAT
    OH SLIM TARG
    OH SMIT RAGL
    OH STAG MIRL
    OH TAGS MIRL
    RAGS HOLM IT
    RAGS LOT HIM
    RAGS MOTH LI
    RAIL GHOST M
    RAIL GOT SHM
    RASH GILT OM
    RASH GOT LIM
    RIAL GHOST M
    RIAL GOT SHM
    RIGS LOAM HT
    RIGS LOT HAM
    RIGS MATH LO
    RIMS GHOST LA
    RIMS GOTH LA
    RIMS HALO GT
    RIMS HOG ALT
    RIMS HOT GAL
    RIMS HOT LAG
    RIOT GASH LM
    RIOT GRAMS LH
    RIOT HAGS LM
    RIOT SHAG LM
    SALT GRIM HO
    SHAG LOT RIM
    SHAM GIRL OT
    SHAM GIRT LO
    SHAM GRIT LO
    SHAM TROG LI
    SHIRT GOAL M
    SHIRT LAM GO
    SHIRT MOG AL
    SHIRT MORG LA
    SHOT GIRL AM
    SLAT GRIM HO
    SLIM GHOST AR
    SLIM HOST ARG
    SLIM RAGS HOT
    SLIM RATH GO
    SLOT GIRL HAM
    SLOT GRIM AH
    SLOT HARM GI
    SLOT MAR H GI
    SLOT RAG HIM
    SLOT TAG RHIM
    SMIT GIRL HOA
    SMIT Harl Go
    SMIT Hoar Gl
    SMIT Hora Gl
    SMIT RAG HOL
    SMIT TAG HORL
    SORT GHIM AL
    STAG HOLM IR
    STAG LOR HIM
    STAG OHM RIL
    STAR GHOST LIM
    STAR HOLM GI
    STAR HOG LIM
    STIR GOAL HM
    STIR GRAM HOL
    STIR LOAM HG
    STIR ROAM HLG
    STORM GIRL HA
    STORM HAG LI
    STORM Harl Gi
    STORM Hoar Gl
    STORM Hora Gl
    STORM RAG HIL
    STORM TAG HIRL
    TAGS MORL HI
    THRO GIRL MAS
    THRO GRAMS LI
    THRO LAGS RIM
    THRO MARLS GI
    THRO RAGS LIM
    THRO SLAG RIM
    TRAGS HOLM I
    TRAGS LOR HIM
    TRAGS OHM RIL
    TRIM GIRL HASO
    TRIM GOAL HS
    TRIM HOST LAG
    TRIM HOST GAL
    TRIM LOGS AH
    TROG SHAM LI
    """
    target_count = Counter(available_letters)
    solutions = []
    
    try:
        with open(dictionary_file) as f:
            words = [word.strip().upper() for word in f if word.strip()]
    except FileNotFoundError:
        print(f"Error: {dictionary_file} not found.")
        return

    # Pre-filter words based on letter availability and length constraints
    valid_words = []
    for word in words:
        word_count = Counter(word)
        if len(word) > 0 and len(word) <= len(available_letters) - 2 and \
           all(word_count[char] <= target_count[char] for char in word_count):
            valid_words.append((word, word_count))
            
    # Use combinations to find triplets
    for combo_indices in combinations(range(len(valid_words)), 3):
        word1, count1 = valid_words[combo_indices[0]]
        word2, count2 = valid_words[combo_indices[1]]
        word3, count3 = valid_words[combo_indices[2]]
        
        # Ensure words are distinct (although combinations indices guarantee this)
        # Check if the combined count matches the target count
        if count1 + count2 + count3 == target_count:
            # Sort the triplet lexicographically
            triplet = tuple(sorted((word1, word2, word3)))
            solutions.append(triplet)
            
    # Sort the final list of triplets
    solutions.sort()
    
    # Print solutions
    for triplet in solutions:
        print(f"{triplet[0]} {triplet[1]} {triplet[2]}")

if __name__ == '__main__':
    import doctest
    doctest.testmod()

