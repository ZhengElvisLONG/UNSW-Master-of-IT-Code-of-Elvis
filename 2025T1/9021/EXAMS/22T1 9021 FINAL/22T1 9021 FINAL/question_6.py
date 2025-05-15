from collections import defaultdict

# The words in the file are supposed to consist of nothing but letters
# (no apostrophes, no hyphens...), possibly immediately followed by
# a single full stop, exclamation mark, question mark,
# comma, colon or semicolon.
#
# A sentence ends in a full stop, an exclamation mark or a question mark
# (neither in a comma nor in a colon nor in a semicolon).
#
# There can be any amount of space anywhere between words, before the
# first word, and after the last word.
#
# We do not distinguish between words that only differ in cases.
# For instance, millionaires, Millionaires, MILLIONAIRES are
# 3 variants of the same word.
#
# The enumeration of sentences starts with 1.
# Within a given sentence, the enumeration of words starts with 1.
#
# It should all happen naturally, but for a given spotted word:
# - Smaller sentence numbers come before larger sentence numbers.
# - For a given sentence, smaller word numbers come before
#   larger word numbers.
#
# You can assume that filename is the name of a file that exists
# in the working directory. Do NOT use absolute paths. 
#
# The code that is already written makes sure that spotted words
# are output in capitalised form, and in lexicographic order, so
# you do not have to take care of it.

def longest_words(filename):
    '''
    >>> longest_words('edgar_poe_1.txt')
    Connoisseurship:
        Spotted as word number 6 in sentence number 10.
    >>> longest_words('edgar_poe_2.txt')
    Retribution:
        Spotted as word number 6 in sentence number 4.
    Unredressed:
        Spotted as word number 4 in sentence number 4.
        Spotted as word number 4 in sentence number 5.
    >>> longest_words('oscar_wild_1.txt')
    Establishment:
        Spotted as word number 9 in sentence number 1.
    Individualism:
        Spotted as word number 17 in sentence number 23.
    Sentimentally:
        Spotted as word number 12 in sentence number 9.
    >>> longest_words('oscar_wild_2.txt')
    Incomparable:
        Spotted as word number 78 in sentence number 1.
        Spotted as word number 83 in sentence number 1.
    Intelligence:
        Spotted as word number 11 in sentence number 6.
    Surroundings:
        Spotted as word number 28 in sentence number 12.
    '''
    longest_words = defaultdict(list)
    
    with open(filename, 'r') as f:
        text = f.read().strip()
    
    # 分割句子（不使用正则表达式）
    sentences = []
    current_sentence = []
    sentence_end = False
    
    for char in text:
        if char in '.!?':
            sentence_end = True
            current_sentence.append(char)
        elif char in ',:;':
            current_sentence.append(' ')  # 用空格替换标点
        elif char.isspace():
            if sentence_end:
                # 完成一个句子
                sentences.append(''.join(current_sentence))
                current_sentence = []
                sentence_end = False
            else:
                current_sentence.append(' ')
        else:
            current_sentence.append(char.lower())  # 统一转换为小写
    
    # 添加最后一个句子（如果存在）
    if current_sentence:
        sentences.append(''.join(current_sentence))
    
    max_length = 0
    word_positions = defaultdict(list)
    
    for sentence_nb, sentence in enumerate(sentences, 1):
        # 分割单词
        words = []
        current_word = []
        
        for char in sentence:
            if char.isalpha():
                current_word.append(char)
            elif current_word:  # 遇到非字母字符且当前有单词
                word = ''.join(current_word)
                words.append(word)
                current_word = []
        
        # 添加最后一个单词（如果存在）
        if current_word:
            word = ''.join(current_word)
            words.append(word)
        
        # 记录单词位置
        for word_nb, word in enumerate(words, 1):
            word_length = len(word)
            word_positions[word].append((sentence_nb, word_nb))
            
            # 更新最大长度
            if word_length > max_length:
                max_length = word_length
    
    # 筛选出最长单词
    for word in word_positions:
        if len(word) == max_length:
            longest_words[word] = word_positions[word]
    
    # 按字母顺序输出
    for word in sorted(longest_words):
        print(f'{word.capitalize()}:')
        for sentence_nb, word_nb in longest_words[word]:
            print(f'    Spotted as word number {word_nb} in sentence '
                  f'number {sentence_nb}.'
                 )

if __name__ == '__main__':
    import doctest
    doctest.testmod()
