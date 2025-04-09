# Encode 0 as 100.
# Given a strictly positive integer n that in base 2,
# reads as b_{1} ... b_{k},
# - encode -n as the integer that in base 2,
#   reads as b_{1}b_{1} ... b_{k}b_{k},
# - encode n as the integer that in base 2,
#   reads as 1b_{1}b_{1} ... b_{k}b_{k}.
# Encode the empty sequence as 0.
# Given an integer n, let the encoding of n also be the encoding of [n].
# Given a list L = [n_{1}, ..., n_{i}] of integers with i > 1,
# encode L as the integer that in base 2, reads as
# c_{1}s_{1}...c_{i-i}s_{i-1}c_{i} where
# - c_1 is the sequence of bits that encodes n_{1}, ...,
#   c_{i} is the sequence of bits that encodes n_{i},
# - s_{1} is 10 if n_2 < 0, and s_{1} is 0 otherwise, ...,
#   s_{i-1} is 10 if n_{i} < 0, and s_{i-1} is 0 otherwise.
#
# Implements a function encode() that takes a list of integers
# as argument, and returns its encoding.
#
# Implements a function decode() that takes an integer n as argument
# and returns None if n does not encode a list,
# and returns the list it encodes otherwise.
#
# Implements a function proportion_of_valid_codes() that takes
# either one integer n at least equal to 0 as argument
# or two integers m and n at least equal to 0 as arguments
# with n at least equal to m,
# that returns what the function says for potential codes
# ranging between 0 and n included in the first case,
# between m and n included in the second case.

import sys
def encode_one_number(n):
    result = ''
    # Encode 0 as 100
    if n == 0:
        return '100'
    
    # Encode positive numbers leading with 1 and repeat each binarized number
    if n > 0:
        n = bin(n)[2:]
        # 对每一位都进行一次重复
        for digit in n:
            result += 2 * digit
        return '1' + result
    
    # Encode negative numbers repeat each binarized opposite number
    if n < 0:
        n = bin(-n)[2:]
        # 对每一位都进行一次重复
        for digit in n:
            result += 2 * digit
        return result
    return 0

def encode(L):
    # 1. Encode 0 as 100
    # 2. Encode positive numbers leading with 1 and repeat each binarized number
    # 3. Encode negative numbers repeat each binarized opposite number
    # 4. Encode [] as 0
    if type(L) == int:
        return encode([L])
    if not L:
        return 0
    result = str(encode_one_number(L[0]))
    for n in L[1:]:
        if n >= 0:
            result += '0' + encode_one_number(n)
        else:
            result += '10' + encode_one_number(n)
    return int(result ,2)

def decode_one_number(binary):
    # 检查二进制是否以'100'开头但不完全是'100'
    if binary[:3] == '100' and binary != '100':
        return None
    # 如果二进制太短或以'0'开头则返回None
    if len(binary) < 2 or binary[0] == '0':
        return None
    # 默认符号为负数
    sign = -1
    number = ''
    # 如果二进制以'1'开头且长度为奇数，则为正数
    if binary[0] == '1' and len(binary) % 2 == 1:
        sign = 1
        binary = binary[1:]  # 移除第一位
    # 特殊情况：'100'表示0
    if binary == '100':
        return 0
    # 成对处理二进制位
    for i in range(0, len(binary), 2):
        # 如果一对位不匹配，返回None（无效编码）
        if binary[i] != binary[i + 1]: 
            return None
        # 从每对中添加一位来构建数字
        number += binary[i]  # 也可以用binary[i+1]，因为它们相同
    # 将二进制数转换为十进制并应用符号
    return sign * int(number, 2)
    
def get_number(bin_str, is_negative=False):
    num, start = "", 0 if is_negative else 1  # 负数从索引0开始，正数从索引1开始
    while start + 1 < len(bin_str) and bin_str[start] == bin_str[start + 1]:
        num += bin_str[start] * 2  # 处理成对的相同位
        start += 2
    return "1" + num if not is_negative else num  # 正数需要前导'1'

def support_decode(bin_str, pos_next):
    lst = []
    while bin_str:
        num = get_number(bin_str, not pos_next)
        real_num = decode_one_number(num)
        if real_num is None: return None
        lst.append(real_num)
        bin_str = bin_str[len(num):]
        if not bin_str: break
        if bin_str[0] == '0': pos_next, bin_str = True, bin_str[1:]
        elif bin_str[:2] == '10': pos_next, bin_str = False, bin_str[2:]
        else: return None
        if not bin_str: return None
    return lst

def decode(num):
    if num < 0: return None  # 不能解码负数
    if num == 0: return []  # 对于零返回空列表
    bin_str = bin(num)[2:]  # 转换为二进制字符串
    for sign in (True, False):
        res = support_decode(bin_str, sign)
        if res is not None: return res
    return None

def proportion_of_valid_codes(*args):
    if len(args) ==1:
        start = 0
        end = args[0] + 1
    else:
        start = args[0]
        end = args[1] + 1
    count = 0
    for i in range(start, end):
        if decode(i) != None:
            count += 1
    return count / (end - start)
