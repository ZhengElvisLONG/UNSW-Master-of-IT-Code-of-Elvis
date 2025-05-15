# Exercise 5: Max Sum Path in Grid
# A grid of numbers is generated based on a seed and density.
# We want to find a path from any cell in the first row (row 0)
# to any cell in the last row (row dim-1) that maximizes the sum of the values
# in the cells along the path.
# A path can only move South (S), South-West (SW), or South-East (SE).
# A path can only move through cells containing non-zero values.
# Output the maximum sum found. If no path exists, output that.
# Also, display a grid showing one such path with the maximum sum, marking path cells with ".".
#
# You can assume that max_sum_path() is called with an integer as first
# argument, an integer at least equal to 1 as second argument.
# The grid dimension (dim) is fixed at 10.
#
# Note that <BLANKLINE> is not output by the program, but
# doctest's way to refer to an empty line.

from random import seed, randrange
import sys

dim = 10

def display_grid_max_sum(grid, path_coords=None):
    # Helper function to display the grid
    max_val_len = 1
    for r in range(dim):
        for c in range(dim):
             if grid[r][c] is not None:
                 max_val_len = max(max_val_len, len(str(grid[r][c])))
                 
    print("   ", "-" * ((max_val_len + 1) * dim + 1))
    for i in range(dim):
        print("   |", end="")
        for j in range(dim):
            char_to_print = " ".rjust(max_val_len)
            if path_coords and (i, j) in path_coords:
                # Use dot for path, keep alignment
                char_to_print = ".".rjust(max_val_len)
            elif grid[i][j] is not None and grid[i][j] != 0:
                 char_to_print = str(grid[i][j]).rjust(max_val_len)
            elif grid[i][j] == 0:
                 char_to_print = "0".rjust(max_val_len) # Show 0s explicitly
            print(f" {char_to_print}", end="")
        print(" |", end="\n")
    print("   ", "-" * ((max_val_len + 1) * dim + 1))

def max_sum_path(for_seed, density):
    """
    Finds a path from the top row to the bottom row with the maximum sum.
    Moves allowed: S, SW, SE. Only through non-zero cells.
    Displays the grid and one path with the maximum sum marked with ".".
    
    >>> max_sum_path(0, 2) # Sparse grid
    Here is the grid that has been generated:
        -----------------------
       |  0  1     3  4  5  6  7  8    |
       |     1     4     6        9 |
       |  0     2  3  4     6  7  8    |
       |        2     4  5     7       |
       |           3        6  7     9 |
       |  0     2     4  5     7  8    |
       |  0              5  6          |
       |           3  4        7  8  9 |
       |  0  1     3     5  6          |
       |  0        3     5  6          |
        -----------------------
    <BLANKLINE>
    Maximum sum found: 46
    Here is one path with the maximum sum:
        -----------------------
       |  0  1     3  4  5  6  .  8    |
       |     1     4     6        . |
       |  0     2  3  4     6  .  8    |
       |        2     4  5     .       |
       |           3        6  .     9 |
       |  0     2     4  5     .  8    |
       |  0              5  .          |
       |           3  4        .  8  9 |
       |  0  1     3     5  .          |
       |  0        3     5  .          |
        -----------------------
    >>> max_sum_path(0, 4) # Denser grid
    Here is the grid that has been generated:
        -----------------------
       |  0  1     3  4  5  6  7  8  9 |
       |  0  1  2     4  5  6        9 |
       |  0     2  3  4  5  6  7  8    |
       |        2     4  5  6  7     9 |
       |  0  1  2  3        6  7     9 |
       |  0     2  3  4  5     7  8  9 |
       |  0  1  2  3     5  6        9 |
       |  0        3  4  5  6  7  8  9 |
       |  0  1     3     5  6  7  8    |
       |  0     2  3  4  5  6        9 |
        -----------------------
    <BLANKLINE>
    Maximum sum found: 64
    Here is one path with the maximum sum:
        -----------------------
       |  0  1     3  4  5  6  7  .  9 |
       |  0  1  2     4  5  6        . |
       |  0     2  3  4  5  6  7  .    |
       |        2     4  5  6  .     9 |
       |  0  1  2  3        6  .     9 |
       |  0     2  3  4  5     .  8  9 |
       |  0  1  2  3     5  .        9 |
       |  0        3  4  5  .  7  8  9 |
       |  0  1     3     5  .  7  8    |
       |  0     2  3  4  5  .        9 |
        -----------------------
    >>> max_sum_path(1, 5) # Very dense grid
    Here is the grid that has been generated:
        -----------------------
       |  0  1  2  3  4  5  6  7  8  9 |
       |  0  1  2  3  4  5  6  7  8  9 |
       |  0  1  2  3  4  5  6  7  8  9 |
       |  0  1  2  3  4  5  6  7  8  9 |
       |  0  1  2  3  4  5  6  7  8  9 |
       |  0  1  2  3  4  5  6  7  8  9 |
       |  0  1  2  3  4  5  6  7  8  9 |
       |  0  1  2  3  4  5  6  7  8  9 |
       |  0  1  2  3  4  5  6  7  8  9 |
       |  0  1  2  3  4  5  6  7  8  9 |
        -----------------------
    <BLANKLINE>
    Maximum sum found: 81
    Here is one path with the maximum sum:
        -----------------------
       |  0  1  2  3  4  5  6  7  8  . |
       |  0  1  2  3  4  5  6  7  8  . |
       |  0  1  2  3  4  5  6  7  8  . |
       |  0  1  2  3  4  5  6  7  8  . |
       |  0  1  2  3  4  5  6  7  8  . |
       |  0  1  2  3  4  5  6  7  8  . |
       |  0  1  2  3  4  5  6  7  8  . |
       |  0  1  2  3  4  5  6  7  8  . |
       |  0  1  2  3  4  5  6  7  8  . |
       |  0  1  2  3  4  5  6  7  8  . |
        -----------------------
    >>> max_sum_path(5, 1) # Extremely sparse grid, likely no path
    Here is the grid that has been generated:
        -----------------------
       |                       |
       |                       |
       |                       |
       |                       |
       |                       |
       |                       |
       |                       |
       |                       |
       |                       |
       |                       |
        -----------------------
    <BLANKLINE>
    No path found.
    """
    seed(for_seed)
    grid = [[randrange(10) if randrange(density) != 0 else 0 for _ in range(dim)]
                 for _ in range(dim)
           ]
    print("Here is the grid that has been generated:")
    display_grid_max_sum(grid)
    print()

    # DP approach: dp[r][c] stores the max sum ending at (r, c)
    # and the path taken to reach it.
    dp = [[(0, []) for _ in range(dim)] for _ in range(dim)]
    max_overall_sum = -1
    best_path_coords = None

    # Initialize first row
    for c in range(dim):
        if grid[0][c] != 0:
            dp[0][c] = (grid[0][c], [(0, c)])

    # Fill DP table row by row
    for r in range(1, dim):
        for c in range(dim):
            if grid[r][c] != 0:
                max_prev_sum = -1
                best_prev_path = []
                # Check possible previous cells (N, NE, NW)
                for dc in [0, -1, 1]:
                    pc = c - dc
                    pr = r - 1
                    if 0 <= pc < dim:
                        prev_sum, prev_path = dp[pr][pc]
                        if prev_sum > 0: # If a valid path reached the previous cell
                            current_sum = prev_sum + grid[r][c]
                            if current_sum > max_prev_sum:
                                max_prev_sum = current_sum
                                best_prev_path = prev_path
                
                if max_prev_sum > 0:
                    dp[r][c] = (max_prev_sum, best_prev_path + [(r, c)])

    # Find the max sum in the last row
    for c in range(dim):
        current_sum, path = dp[dim - 1][c]
        if current_sum > max_overall_sum:
            max_overall_sum = current_sum
            best_path_coords = set(path)

    if max_overall_sum > 0:
        print(f"Maximum sum found: {max_overall_sum}")
        print("Here is one path with the maximum sum:")
        display_grid_max_sum(grid, best_path_coords)
    else:
        print("No path found.")

if __name__ == '__main__':
    import doctest
    doctest.testmod()

