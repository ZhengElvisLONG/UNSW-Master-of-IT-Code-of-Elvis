# Exercise 4: Diamond Pattern with Letters
# Creates a diamond pattern using consecutive letters starting from a given letter.
# The width parameter determines the letter at the widest point (center row).
# For example, width=3 means the center row goes up to the 3rd letter from the start.
# The pattern fills columns outwards from the center, then inwards.
# Letters wrap around from 'Z' to 'A'.
#
# You can assume width is a positive odd integer and starting_from is an uppercase letter.
# Note that NONE OF THE LINES THAT ARE OUTPUT HAS TRAILING SPACES.

def next_letter(letter):
    if letter == 'Z':
        return 'A'
    return chr(ord(letter) + 1)

def prev_letter(letter):
    if letter == 'A':
        return 'Z'
    return chr(ord(letter) - 1)

def diamond_pattern_letters(width, starting_from='A'):
    """
    Creates a diamond pattern using letters.
    
    >>> diamond_pattern_letters(1, 'A')
    A
    >>> diamond_pattern_letters(3, 'A')
     A
    ABA
     A
    >>> diamond_pattern_letters(5, 'C')
      C
     CDC
    CDEDC
     CDC
      C
    >>> diamond_pattern_letters(7, 'X')
       X
      XYX
     XYZYX
    XYZAZYX
     XYZYX
      XYX
       X
    >>> diamond_pattern_letters(3, 'Y')
     Y
    YZY
     Y
    """
    # if width <= 0 or width % 2 == 0:
    #     return
    
    # center_index = width // 2
    # current_letter = starting_from
    
    # # Upper part including center
    # for i in range(center_index + 1):
    #     line = [' '] * width
    #     mid_letter = current_letter
    #     line[center_index] = mid_letter
    #     # Fill left and right
    #     left_letter = mid_letter
    #     right_letter = mid_letter
    #     for j in range(1, i + 1):
    #         left_letter = prev_letter(left_letter)
    #         right_letter = next_letter(right_letter)
    #         line[center_index - j] = left_letter
    #         line[center_index + j] = right_letter
    #     print("".join(line))
    #     if i < center_index:
    #          current_letter = next_letter(current_letter)

    # # Lower part excluding center
    # for i in range(center_index - 1, -1, -1):
    #     line = [' '] * width
    #     mid_letter = prev_letter(current_letter)
    #     current_letter = mid_letter # Update current letter for next iteration down
    #     line[center_index] = mid_letter
    #     # Fill left and right
    #     left_letter = mid_letter
    #     right_letter = mid_letter
    #     for j in range(1, i + 1):
    #         left_letter = prev_letter(left_letter)
    #         right_letter = next_letter(right_letter)
    #         line[center_index - j] = left_letter
    #         line[center_index + j] = right_letter
    #     print("".join(line))
    size = (width + 1) // 2
    result = ["" for _ in range(width)]
    for i in range(size):
        current = starting_from
        result[i] += " " * (size - i - 1)
        for j in range(i + 1):
            result[i] += current
            current = next_letter(current)
        current = prev_letter(current)
        for j in range(i):
            current = prev_letter(current)
            result[i] += current
        
    for i in range(size, width):
        result[i] += " " * (i - size + 1)
        current = starting_from
        for j in range(width - i):
            result[i] += current
            current = next_letter(current)
        current = prev_letter(current)
        for j in range(width - i - 1):
            current = prev_letter(current)
            result[i] += current

    for i in range(width):
        print(result[i])
        
if __name__ == '__main__':
    import doctest
    doctest.testmod()

