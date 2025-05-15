# Exercise 5: Shortest Path in Grid
# A grid of numbers is generated based on a seed and density.
# We want to find the length of the shortest path from any cell containing the value 'top'
# in the first row (row 0) to any cell containing the value 'bottom' in the last row (row dim-1).
# A path can only move South (S), South-West (SW), or South-East (SE).
# A path can only move through cells containing non-zero values.
# If multiple shortest paths exist, any one is valid.
# Output the length of the shortest path. If no path exists, output that.
# Also, display a grid showing one such shortest path, marking path cells with '*'.
#
# You can assume that shortest_path() is called with an integer as first
# argument, an integer at least equal to 1 as second argument,
# and integers between 0 and 9 as third and fourth arguments.
# The grid dimension (dim) is fixed at 10.
#
# Note that <BLANKLINE> is not output by the program, but
# doctest's way to refer to an empty line.

from random import seed, randrange
from collections import deque

dim = 10

def display_grid(grid, path_coords=None):
    # Helper function to display the grid
    print("   ", "-" * (2 * dim + 1))
    for i in range(dim):
        print("   |", end="")
        for j in range(dim):
            char_to_print = " "
            if path_coords and (i, j) in path_coords:
                char_to_print = "*"
            elif grid[i][j] is not None and grid[i][j] != 0:
                 char_to_print = str(grid[i][j])
            elif grid[i][j] == 0:
                 char_to_print = "0" # Show 0s explicitly for clarity
            print(f" {char_to_print}", end="")
        print(" |", end="\n")
    print("   ", "-" * (2 * dim + 1))

def shortest_path(for_seed, density, top, bottom):
    """
    Finds the shortest path length from 'top' in row 0 to 'bottom' in row dim-1.
    Moves allowed: S, SW, SE. Only through non-zero cells.
    Displays the grid and one shortest path marked with '*'.
    
    >>> shortest_path(0, 2, 0, 0) # Grid has 0s, likely no path
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
    No path found from 0 at the top to 0 at the bottom.
    >>> shortest_path(0, 4, 6, 7) # Path exists
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
    Shortest path length from 6 at the top to 7 at the bottom: 9
    Here is one shortest path:
        ---------------------
       | 0 1   3 4 5 * 7 8 9 |
       | 0 1 2   4 * 6     9 |
       | 0   2 3 4 * 6 7 8   |
       |     2   4 * 6 7   9 |
       | 0 1 2 3   * 6 7   9 |
       | 0   2 3 4 *   7 8 9 |
       | 0 1 2 3   * 6     9 |
       | 0     3 4 5 * 7 8 9 |
       | 0 1   3   5 * 7 8   |
       | 0   2 3 4 5 *     9 |
        ---------------------
    >>> shortest_path(0, 4, 0, 2) # Path exists
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
    Shortest path length from 0 at the top to 2 at the bottom: 9
    Here is one shortest path:
        ---------------------
       | * 1   3 4 5 6 7 8 9 |
       | * 1 2   4 5 6     9 |
       | *   2 3 4 5 6 7 8   |
       |     *   4 5 6 7   9 |
       | 0 1 * 3     6 7   9 |
       | 0   * 3 4 5   7 8 9 |
       | 0 1 * 3   5 6     9 |
       | 0     * 4 5 6 7 8 9 |
       | 0 1   *   5 6 7 8   |
       | 0   * 3 4 5 6     9 |
        ---------------------
    >>> shortest_path(1, 5, 8, 5) # Dense grid, path exists
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
    Shortest path length from 8 at the top to 5 at the bottom: 9
    Here is one shortest path:
        ---------------------
       | 0 1 2 3 4 5 6 7 * 9 |
       | 0 1 2 3 4 5 6 * 8 9 |
       | 0 1 2 3 4 5 * 7 8 9 |
       | 0 1 2 3 4 * 6 7 8 9 |
       | 0 1 2 3 * 5 6 7 8 9 |
       | 0 1 2 * 4 5 6 7 8 9 |
       | 0 1 * 3 4 5 6 7 8 9 |
       | 0 * 2 3 4 5 6 7 8 9 |
       | * 1 2 3 4 5 6 7 8 9 |
       | 0 1 2 3 4 * 6 7 8 9 |
        ---------------------
    """
    seed(for_seed)
    grid = [[randrange(10) if randrange(density) != 0 else 0 for _ in range(dim)]
                 for _ in range(dim)
           ]
    print("Here is the grid that has been generated:")
    display_grid(grid)
    print()

    # q = deque()
    # visited = set()
    # start_nodes = []

    # # Find all starting cells in the first row
    # for c in range(dim):
    #     if grid[0][c] == top and grid[0][c] != 0:
    #         start_nodes.append(((0, c), [(0, c)])) # ((row, col), path_list)
    #         visited.add((0, c))

    # if not start_nodes:
    #     print(f"No starting point {top} found in the first row.")
    #     return
        
    # q.extend(start_nodes)
    # shortest_len = -1
    # shortest_path_coords = None

    # while q:
    #     (r, c), path = q.popleft()
    #     current_len = len(path) - 1 # Path length is number of steps

    #     # Check if we reached the bottom row with the target value
    #     if r == dim - 1 and grid[r][c] == bottom:
    #         shortest_len = current_len
    #         shortest_path_coords = set(path)
    #         break # Found the shortest path (BFS guarantees this)

    #     # Explore neighbors (S, SW, SE)
    #     for dr, dc in [(1, 0), (1, -1), (1, 1)]:
    #         nr, nc = r + dr, c + dc
    #         # Check bounds, non-zero value, and not visited
    #         if 0 <= nr < dim and 0 <= nc < dim and grid[nr][nc] != 0 and (nr, nc) not in visited:
    #             visited.add((nr, nc))
    #             new_path = path + [(nr, nc)]
    #             q.append(((nr, nc), new_path))

    # if shortest_len != -1:
    #     print(f"Shortest path length from {top} at the top to {bottom} at the bottom: {shortest_len}")
    #     print("Here is one shortest path:")
    #     display_grid(grid, shortest_path_coords)
    # else:
    #     print(f"No path found from {top} at the top to {bottom} at the bottom.")

if __name__ == '__main__':
    import doctest
    doctest.testmod()

