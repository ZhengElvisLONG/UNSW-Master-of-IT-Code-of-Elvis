# Exercise 5: Count Paths in Grid
# A grid of numbers is generated based on a seed and density.
# We want to count the number of distinct paths from any cell containing the value 'top'
# in the first row (row 0) to any cell containing the value 'bottom' in the last row (row dim-1).
# A path can only move South (S), South-West (SW), or South-East (SE).
# A path can only move through cells containing non-zero values.
#
# You can assume that paths() is called with an integer as first
# argument, an integer at least equal to 1 as second argument,
# and integers between 0 and 9 as third and fourth arguments.
# The grid dimension (dim) is fixed at 10.
#
# Note that <BLANKLINE> is not output by the program, but
# doctest's way to refer to an empty line.

from random import seed, randrange
dim = 10

def display(grid):
    # Helper function to display the grid (optional, can be removed if not needed for debugging)
    print("   ", "-" * (2 * dim + 1))
    for i in range(dim):
        print("   |", " ".join(str(grid[i][j]) if grid[i][j] is not None else " "
                                   for j in range(dim)
                              ), end=" |\n"
             )
    print("   ", "-" * (2 * dim + 1))

def count_paths(for_seed, density, top, bottom):
    """
    Counts the number of paths from 'top' in the first row to 'bottom' in the last row.
    Moves allowed: S, SW, SE. Only through non-zero cells.
    
    >>> count_paths(0, 2, 0, 0)
    Here is the grid that has been generated:
        ---------------------
       | 0 1   3 4 5 6 7 8   |
       |   1     4   6     9 |
       | 0   2 3 4   6 7 8   |
       |     2   4 5   7     |
       |       3     6 7   9 |
       | 0   2   4 5   7 8   |
       | 0         5 6       |
       |       3 4     7 8 9 |
       | 0 1   3   5 6       |
       | 0     3   5 6       |
        ---------------------
    <BLANKLINE>
    Number of paths from 0 at the top to 0 at the bottom: 0
    >>> count_paths(0, 4, 6, 7)
    Here is the grid that has been generated:
        ---------------------
       | 0 1   3 4 5 6 7 8 9 |
       | 0 1 2   4 5 6     9 |
       | 0   2 3 4 5 6 7 8   |
       |     2   4 5 6 7   9 |
       | 0 1 2 3     6 7   9 |
       | 0   2 3 4 5   7 8 9 |
       | 0 1 2 3   5 6     9 |
       | 0     3 4 5 6 7 8 9 |
       | 0 1   3   5 6 7 8   |
       | 0   2 3 4 5 6     9 |
        ---------------------
    <BLANKLINE>
    Number of paths from 6 at the top to 7 at the bottom: 7
    >>> count_paths(0, 4, 6, 6)
    Here is the grid that has been generated:
        ---------------------
       | 0 1   3 4 5 6 7 8 9 |
       | 0 1 2   4 5 6     9 |
       | 0   2 3 4 5 6 7 8   |
       |     2   4 5 6 7   9 |
       | 0 1 2 3     6 7   9 |
       | 0   2 3 4 5   7 8 9 |
       | 0 1 2 3   5 6     9 |
       | 0     3 4 5 6 7 8 9 |
       | 0 1   3   5 6 7 8   |
       | 0   2 3 4 5 6     9 |
        ---------------------
    <BLANKLINE>
    Number of paths from 6 at the top to 6 at the bottom: 13
    >>> count_paths(0, 4, 0, 2)
    Here is the grid that has been generated:
        ---------------------
       | 0 1   3 4 5 6 7 8 9 |
       | 0 1 2   4 5 6     9 |
       | 0   2 3 4 5 6 7 8   |
       |     2   4 5 6 7   9 |
       | 0 1 2 3     6 7   9 |
       | 0   2 3 4 5   7 8 9 |
       | 0 1 2 3   5 6     9 |
       | 0     3 4 5 6 7 8 9 |
       | 0 1   3   5 6 7 8   |
       | 0   2 3 4 5 6     9 |
        ---------------------
    <BLANKLINE>
    Number of paths from 0 at the top to 2 at the bottom: 1
    >>> count_paths(1, 5, 8, 5)
    Here is the grid that has been generated:
        ---------------------
       | 0 1 2 3 4 5 6 7 8 9 |
       | 0 1 2 3 4 5 6 7 8 9 |
       | 0 1 2 3 4 5 6 7 8 9 |
       | 0 1 2 3 4 5 6 7 8 9 |
       | 0 1 2 3 4 5 6 7 8 9 |
       | 0 1 2 3 4 5 6 7 8 9 |
       | 0 1 2 3 4 5 6 7 8 9 |
       | 0 1 2 3 4 5 6 7 8 9 |
       | 0 1 2 3 4 5 6 7 8 9 |
       | 0 1 2 3 4 5 6 7 8 9 |
        ---------------------
    <BLANKLINE>
    Number of paths from 8 at the top to 5 at the bottom: 120
    """
    seed(for_seed)
    # Generate grid with numbers 0-9 based on density, 0 means blocked
    grid = [[randrange(10) if randrange(density) != 0 else 0 for _ in range(dim)]
                 for _ in range(dim)
           ]
    print("Here is the grid that has been generated:")
    display(grid)
    print()

    memo = {}

    def find_paths_from(r, c):
        # Check if out of bounds or current cell is blocked (0)
        if r < 0 or r >= dim or c < 0 or c >= dim or grid[r][c] == 0:
            return 0
        
        # Check if this is the last row
        if r == dim - 1:
            return 1 if grid[r][c] == bottom else 0
            
        # Check memoization table
        if (r, c) in memo:
            return memo[(r, c)]

        # Recursive calls for S, SW, SE moves
        count = find_paths_from(r + 1, c) + \
                find_paths_from(r + 1, c - 1) + \
                find_paths_from(r + 1, c + 1)
        
        # Store result in memoization table
        memo[(r, c)] = count
        return count

    total_paths = 0
    # Iterate through the first row to find starting points
    for c_start in range(dim):
        if grid[0][c_start] == top:
            # Reset memo for each starting point to count distinct paths correctly
            # Or rather, the memo should store counts *to the end* from (r,c)
            # so it can be reused across different starting points.
            memo = {} # Re-initialize memo for path counting from this start point
            
            # Need a slightly different approach: DP from bottom-up or top-down with memo
            # Let dp[r][c] be the number of paths from (r, c) to any 'bottom' in the last row.
            
            dp = {} # Use dictionary for sparse memoization

            def count_recursive(row, col):
                # Base cases
                if row < 0 or row >= dim or col < 0 or col >= dim or grid[row][col] == 0:
                    return 0
                if row == dim - 1:
                    return 1 if grid[row][col] == bottom else 0
                
                # Check memo
                if (row, col) in dp:
                    return dp[(row, col)]
                
                # Recursive step
                paths_count = count_recursive(row + 1, col) + \
                              count_recursive(row + 1, col - 1) + \
                              count_recursive(row + 1, col + 1)
                
                dp[(row, col)] = paths_count
                return paths_count

            total_paths += count_recursive(0, c_start)

    print(f"Number of paths from {top} at the top to {bottom} at the bottom: {total_paths}")

if __name__ == '__main__':
    import doctest
    doctest.testmod()

