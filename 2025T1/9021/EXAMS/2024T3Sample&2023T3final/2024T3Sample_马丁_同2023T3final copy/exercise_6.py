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
# 手搓字典版
    # 1. 读文件并排序字典
    result = []
    with open("dictionary.txt", 'r') as f:
        words = [word.strip().upper() for word in f if word.strip()] # 要strip和upper，记住以列表形式
    words.sort()
    # 2. set dictionary for available letters
    dic = {}
    ch = 'A'
    letters = set()
    for _ in range(26): # 初始化
        dic[ch] = 0
        ch = chr(ord(ch) + 1)
    for ch in available_letters: # 处理好available_letters
        dic[ch] += 1
        letters.add(ch)
    # 3. 找word1和word2
    ok1, ok2 = False, False # ！！！
    for word1 in words:
        ok1 = True
        # 需要用copy函数copy字典！！！
        dic_cp = dic.copy()
        for ch in word1:
            if dic_cp[ch]:
                dic_cp[ch] -= 1
            else: # 如果对不上直接break
                ok1 = False
                break
        if not ok1: # 如果对不上到下一轮，因为外面已经是大循环了不能break
            ok, ok2 = False, False
            # 看清楚哪里需要continue哪里需要break，word1对完了才continue
            continue
        for word2 in words:
            # 查word2的时候还要copy一次字典
            dic_cp2 = dic_cp.copy()
            ok2 = True
            for ch in word2:
                if dic_cp2[ch] != 0:
                    dic_cp2[ch] -= 1
                else:
                    ok2 = False
                    break # break还是continue主要看循环的层
            if not ok2:
                ok = False
                continue
            ok = True
            for ch in letters:
                if dic_cp2[ch] != 0 or not ok1 or not ok2: # 注意不仅是ok还要判断是否判完
                    ok = False
                    break
                # 两个词不能是一样的，并且要提前排序
            if ok and word1 != word2:
                word_tuple = sorted([word1, word2])
                result.append((word_tuple[0], word_tuple[1])) # 注意一定是append元组
    # 4. 去重、排序、输出
    result = list(set(result))
    result.sort()
    for pair in result:
        print(f"{pair[0]} {pair[1]}")

'''用counter版'''
    # # 1. 统计输入字母的频次
    # # Counter会生成类似字典的结构，如 {'h':1, 'e':1, 'l':2, 'o':1}
    # target_count = Counter(available_letters.upper())  # 统一转为大写
    # solutions = []  # 存储最终结果
    
    # # 2. 读取字典文件并预处理
    # with open('dictionary.txt') as f:
    #     # 处理每行：去除首尾空格、转大写、跳过空行，要储存成列表
    #     words = [word.strip().upper() for word in f if word.strip()]
    
    # # 3. 筛选可能单词（核心逻辑）
    # valid_words = []  # 存储符合条件的单词及其计数
    # for word in words:
    #     word_count = Counter(word)  # 统计当前单词字母频次
        
    #     # all()检查单词每个字母的计数是否都<=可用字母计数
    #     # 例如：单词"HELL"的L计数为2 <= 输入"HELLO"的L计数2 → 符合
    #     is_valid = all(word_count[char] <= target_count[char] 
    #                   for char in word_count)
        
    #     if is_valid:
    #         valid_words.append((word, word_count))  # 存储单词及其计数
    
    # # 4. 查找所有有效双词组合（核心逻辑）
    # for i, (word1, count1) in enumerate(valid_words):
    #     # 计算剩余可用字母 = 总字母 - 第一个单词的字母
    #     remaining = target_count - count1  # Counter支持减法运算
        
    #     # 遍历后续单词（避免重复检查）
    #     for j, (word2, count2) in enumerate(valid_words[i+1:], i+1):
    #         # 检查第二个单词是否正好用完剩余字母
    #         # 且按字母顺序排列避免重复（如HELLO WORLD和WORLD HELLO）
    #         if count2 == remaining and word1 < word2:
    #             solutions.append((word1, word2))
    
    # # 5. 结果处理与输出
    # solutions.sort()  # 按字母顺序排序
    # for pair in solutions:
    #     print(f"{pair[0]} {pair[1]}")  # 按要求格式输出


# Counter使用示例说明：
"""
Counter是collections模块提供的强大工具，常用方法：

1. 创建计数器：
   c = Counter('hello') → {'h':1, 'e':1, 'l':2, 'o':1}

2. 元素访问：
   c['l'] → 2 (不存在的key返回0，不会报错)

3. 数学运算：
   - 加法：c1 + c2 → 合并计数
   - 减法：c1 - c2 → 扣除计数（结果中只保留正数）
   - 交集：c1 & c2 → 取各key的最小值
   - 并集：c1 | c2 → 取各key的最大值

4. 常用方法：
   - most_common(n): 返回前n个最常见元素
   - elements(): 返回所有元素的迭代器
   - subtract(): 原地减法操作
"""

'''双重字典'''
    # # 1. read file
    # result = []
    # with open(dictionary_file, 'r') as f:
    #     words = sorted([word.upper().strip() for word in f if word.strip()])
    # # 2. make dictionary
    # letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    # dic = {}
    # word_dic = {}
    # for ch in letters:
    #     dic[ch] = 0
    # for ch in available_letters:
    #     dic[ch] += 1
    # for word in words:
    #     word_dic[word] = {}
    #     for ch in letters:
    #         word_dic[word][ch] = 0
    #     for ch in word:
    #         word_dic[word][ch] += 1
    # # 3. match word1
    # for i in range(len(words)):
    #     word1 = words[i]
    #     word1_ok = True
    #     dic_cp1 = dic.copy()
    #     for ch in word1:
    #         if word_dic[word1][ch] <= dic_cp1[ch]:
    #             dic_cp1[ch] -= word_dic[word1][ch]
    #         else:
    #             word1_ok = False
    #             break
    #     if word1_ok == False:
    #         continue
    # # 4. match word2
    #     for j in range(i, len(words)):
    #         word2 = words[j]
    #         word2_ok = True
    #         dic_cp2 = dic_cp1.copy()
    #         for ch in word2:
    #             if word_dic[word2][ch] <= dic_cp2[ch]:
    #                 dic_cp2[ch] -= word_dic[word2][ch]
    #             else:
    #                 word2_ok = False
    #                 break
    #         for ch in letters:
    #             if dic_cp2[ch] != 0:
    #                 word2_ok = False
    #         if word2_ok == False:
    #             continue
    # # 5. sorted tuples and sorted results
    #         if word1_ok and word2_ok and word1 != word2:
    #             ans = sorted([word1, word2])
    #             result.append((ans[0], ans[1]))
    # result = list(set(result))
    # result.sort()
    # for pair in result:
    #     print(f"{pair[0]} {pair[1]}")
if __name__ == '__main__':
    import doctest
    doctest.testmod()
