

def f(word):
    '''
    Recall that if c is an ascii character then ord(c) returns its ascii code.
    Will be tested on nonempty strings of lowercase letters only.

    >>> f('x')
    The longest substring of consecutive letters has a length of 1.
    The leftmost such substring is x.
    >>> f('xy')
    The longest substring of consecutive letters has a length of 2.
    The leftmost such substring is xy.
    >>> f('ababcuvwaba')
    The longest substring of consecutive letters has a length of 3.
    The leftmost such substring is abc.
    >>> f('abbcedffghiefghiaaabbcdefgg')
    The longest substring of consecutive letters has a length of 6.
    The leftmost such substring is bcdefg.
    >>> f('abcabccdefcdefghacdef')
    The longest substring of consecutive letters has a length of 6.
    The leftmost such substring is cdefgh.
    '''
    desired_length = 0
    desired_substring = ''
    # Insert your code here
    if word:
        desired_length = 1
        temp_substring = word[0]
        temp_length = 1
        for i in range(1,len(word)):
            if ord(temp_substring[-1]) + 1 == ord(word[i]):
                temp_substring+=word[i]
                temp_length +=1
            else:
                desired_length = max(temp_length,desired_length)
                if len(temp_substring) > len(desired_substring):
                    desired_substring = temp_substring

                temp_length = 1
                temp_substring = word[i]
                
        desired_length = max(temp_length,desired_length)
        if len(temp_substring) > len(desired_substring):
            desired_substring = temp_substring
    print(f'The longest substring of consecutive letters has a length of {desired_length}.')
    print(f'The leftmost such substring is {desired_substring}.')

if __name__ == '__main__':
    import doctest
    doctest.testmod()
