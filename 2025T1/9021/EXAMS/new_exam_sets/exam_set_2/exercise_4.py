# Exercise 4: Spiral Rectangle Pattern
# Creates a spiral pattern using consecutive letters starting from a given letter.
# The spiral starts from the top-left corner and moves clockwise inwards.
# The pattern fills a rectangle of size width x height.
# Letters wrap around from 'Z' to 'A'.
#
# You can assume width and height are integers >= 0, and starting_from is an uppercase letter.
# Note that NONE OF THE LINES THAT ARE OUTPUT HAS TRAILING SPACES.

def next_letter(letter):
    if letter == 'Z':
        return 'A'
    return chr(ord(letter) + 1)

def spiral_rectangle(width, height, starting_from='A'):
    """
    Creates a clockwise spiral pattern of letters in a rectangle.
    
    >>> spiral_rectangle(0, 0)
    >>> spiral_rectangle(1, 1, 'X')
    X
    >>> spiral_rectangle(3, 1, 'A')
    ABC
    >>> spiral_rectangle(1, 4, 'P')
    P
    Q
    R
    S
    >>> spiral_rectangle(3, 3, 'A')
    ABC
    HI 
    GFE
    >>> spiral_rectangle(4, 3, 'A')
    ABCD
    JK L
    IHGF
    >>> spiral_rectangle(5, 4, 'M')
    MNOPQ
    X YZR
    W VUTS
      
    >>> spiral_rectangle(6, 5, 'T')
    TUVWXY
    KLMN Z
    J OPQA
    I HGFEB
      DC
    """
    # if width <= 0 or height <= 0:
    #     return

    # grid = [[' ' for _ in range(width)] for _ in range(height)]
    # top, bottom, left, right = 0, height - 1, 0, width - 1
    # direction = 0  # 0: right, 1: down, 2: left, 3: up
    # current_letter = starting_from
    # count = 0
    # total_cells = width * height

    # while top <= bottom and left <= right and count < total_cells:
    #     if direction == 0:  # Move right
    #         for i in range(left, right + 1):
    #             if count < total_cells:
    #                 grid[top][i] = current_letter
    #                 current_letter = next_letter(current_letter)
    #                 count += 1
    #         top += 1
    #     elif direction == 1:  # Move down
    #         for i in range(top, bottom + 1):
    #              if count < total_cells:
    #                 grid[i][right] = current_letter
    #                 current_letter = next_letter(current_letter)
    #                 count += 1
    #         right -= 1
    #     elif direction == 2:  # Move left
    #         for i in range(right, left - 1, -1):
    #              if count < total_cells:
    #                 grid[bottom][i] = current_letter
    #                 current_letter = next_letter(current_letter)
    #                 count += 1
    #         bottom -= 1
    #     elif direction == 3:  # Move up
    #         for i in range(bottom, top - 1, -1):
    #              if count < total_cells:
    #                 grid[i][left] = current_letter
    #                 current_letter = next_letter(current_letter)
    #                 count += 1
    #         left += 1
        
    #     direction = (direction + 1) % 4

    # # Print the grid
    # for row in grid:
    #     print("".join(row).rstrip())

if __name__ == '__main__':
    import doctest
    doctest.testmod()

